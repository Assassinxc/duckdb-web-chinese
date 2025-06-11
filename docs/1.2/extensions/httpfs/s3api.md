---
layout: docu
title: S3 API Support
---

The `httpfs` extension supports reading/writing/[globbing](#globbing) files on object storage servers using the S3 API. S3 offers a standard API to read and write to remote files (while regular http servers, predating S3, do not offer a common write API). DuckDB conforms to the S3 API, that is now common among industry storage providers.

## Platforms

The `httpfs` filesystem is tested with [AWS S3](https://aws.amazon.com/s3/), [Minio](https://min.io/), [Google Cloud](https://cloud.google.com/storage/docs/interoperability), and [lakeFS](https://docs.lakefs.io/integrations/duckdb.html). Other services that implement the S3 API (such as [Cloudflare R2](https://www.cloudflare.com/en-gb/developer-platform/r2/)) should also work, but not all features may be supported.

The following table shows which parts of the S3 API are required for each `httpfs` feature.

| Feature | Required S3 API features |
|:---|:---|
| Public file reads | HTTP Range requests |
| Private file reads | Secret key or session token authentication |
| File glob | [ListObjectsV2](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html) |
| File writes | [Multipart upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html) |

## Configuration and Authentication

The preferred way to configure and authenticate to S3 endpoints is to use [secrets]({% link docs/1.2/sql/statements/create_secret.md %}). Multiple secret providers are available.

To migrate from the [deprecated S3 API]({% link docs/1.2/extensions/httpfs/s3api_legacy_authentication.md %}), use a defined secret with a profile.
See the [“Loading a Secret Based on a Profile” section](#loading-a-secret-based-on-a-profile).

### `config` Provider

The default provider, `config` (i.e., user-configured), allows access to the S3 bucket by manually providing a key. For example:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER config,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
);
```

> Tip If you get an IO Error (`Connection error for HTTP HEAD`), configure the endpoint explicitly via `ENDPOINT 's3.⟨your_region⟩.amazonaws.com'`{:.language-sql .highlight}.

Now, to query using the above secret, simply query any `s3://` prefixed file:

```sql
SELECT *
FROM 's3://⟨your_bucket⟩/⟨your_file⟩.parquet';
```

### `credential_chain` Provider

The `credential_chain` provider allows automatically fetching credentials using mechanisms provided by the AWS SDK. For example, to use the AWS SDK default provider:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain
);
```

Again, to query a file using the above secret, simply query any `s3://` prefixed file.

DuckDB also allows specifying a specific chain using the `CHAIN` keyword. This takes a semicolon-separated list (`a;b;c`) of providers that will be tried in order. For example:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN 'env;config'
);
```

The possible values for `CHAIN` are the following:

* [`config`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_profile_config_file_a_w_s_credentials_provider.html)
* [`sts`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_s_t_s_assume_role_web_identity_credentials_provider.html)
* [`sso`](https://aws.amazon.com/what-is/sso/)
* [`env`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_environment_a_w_s_credentials_provider.html)
* [`instance`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_instance_profile_credentials_provider.html)
* [`process`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_process_credentials_provider.html)

The `credential_chain` provider also allows overriding the automatically fetched config. For example, to automatically load credentials, and then override the region, run:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN config,
    REGION '⟨eu-west-1⟩'
);
```

#### Loading a Secret Based on a Profile

To load credentials based on a profile which is not defined as a default from the `AWS_PROFILE` environment variable or as a default profile based on AWS SDK precedence, run:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN config,
    PROFILE '⟨my_profile⟩'
);
```

This approach is equivalent to the [deprecated S3 API's]({% link docs/1.2/extensions/httpfs/s3api_legacy_authentication.md %})'s method `load_aws_credentials('⟨my_profile⟩')`.

### Overview of S3 Secret Parameters

Below is a complete list of the supported parameters that can be used for both the `config` and `credential_chain` providers:

| Name                          | Description                                                                           | Secret            | Type      | Default                                     |
|:------------------------------|:--------------------------------------------------------------------------------------|:------------------|:----------|:--------------------------------------------|
| `ENDPOINT`                    | Specify a custom S3 endpoint                                                          | `S3`, `GCS`, `R2` | `STRING`  | `s3.amazonaws.com` for `S3`,                |
| `KEY_ID`                      | The ID of the key to use                                                              | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `REGION`                      | The region for which to authenticate (should match the region of the bucket to query) | `S3`, `GCS`, `R2` | `STRING`  | `us-east-1`                                 |
| `SECRET`                      | The secret of the key to use                                                          | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `SESSION_TOKEN`               | Optionally, a session token can be passed to use temporary credentials                | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `URL_COMPATIBILITY_MODE`      | Can help when URLs contain problematic characters                                     | `S3`, `GCS`, `R2` | `BOOLEAN` | `true`                                      |
| `URL_STYLE`                   | Either `vhost` or `path`                                                              | `S3`, `GCS`, `R2` | `STRING`  | `vhost` for `S3`, `path` for `R2` and `GCS` |
| `USE_SSL`                     | Whether to use HTTPS or HTTP                                                          | `S3`, `GCS`, `R2` | `BOOLEAN` | `true`                                      |
| `ACCOUNT_ID`                  | The R2 account ID to use for generating the endpoint URL                              | `R2`              | `STRING`  | -                                           |
| `KMS_KEY_ID`                  | AWS KMS (Key Management Service) key for Server Side Encryption S3                    | `S3`              | `STRING`  | -                                           |

### Platform-Specific Secret Types

#### S3 Secrets

The httpfs extension supports [Server Side Encryption via the AWS Key Management Service (KMS) on S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html) using the `KMS_KEY_ID` option:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN config,
    REGION '⟨eu-west-1⟩',
    KMS_KEY_ID 'arn:aws:kms:⟨region⟩:⟨account_id⟩:⟨key⟩/⟨key_id⟩',
    SCOPE 's3://⟨bucket_sub_path⟩'
);
```

#### R2 Secrets

While [Cloudflare R2](https://www.cloudflare.com/developer-platform/r2) uses the regular S3 API, DuckDB has a special Secret type, `R2`, to make configuring it a bit simpler:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE r2,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    ACCOUNT_ID '⟨my_account_id⟩'
);
```

Note the addition of the `ACCOUNT_ID` which is used to generate to correct endpoint URL for you. Also note that for `R2` Secrets can also use both the `CONFIG` and `credential_chain` providers. Finally, `R2` secrets are only available when using URLs starting with `r2://`, for example:

```sql
SELECT *
FROM read_parquet('r2://⟨some_file_that_uses_an_r2_secret⟩.parquet');
```

#### GCS Secrets

While [Google Cloud Storage](https://cloud.google.com/storage) is accessed by DuckDB using the S3 API, DuckDB has a special Secret type, `GCS`, to make configuring it a bit simpler:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE gcs,
    KEY_ID '⟨my_key⟩',
    SECRET '⟨my_secret⟩'
);
```

Note that the above secret, will automatically have the correct Google Cloud Storage endpoint configured. Also note that for `GCS` Secrets can also use both the `CONFIG` and `credential_chain` providers. Finally, `GCS` secrets are only available when using URLs starting with `gcs://` or `gs://`, for example:

```sql
SELECT *
FROM read_parquet('gcs://⟨some/file/that/uses/a/gcs/secret⟩.parquet');
```

## Reading

Reading files from S3 is now as simple as:

```sql
SELECT *
FROM 's3://⟨bucket_name⟩/⟨filename⟩.⟨extension⟩';
```

### Partial Reading

The `httpfs` extension supports [partial reading]({% link docs/1.2/extensions/httpfs/https.md %}#partial-reading) from S3 buckets.

### Reading Multiple Files

Multiple files are also possible, for example:

```sql
SELECT *
FROM read_parquet([
    's3://⟨bucket_name⟩/⟨filename_1⟩.parquet',
    's3://⟨bucket_name⟩/⟨filename_2⟩.parquet'
]);
```

### Globbing

File [globbing]({% link docs/1.2/sql/functions/pattern_matching.md %}#globbing) is implemented using the ListObjectsV2 API call and allows to use filesystem-like glob patterns to match multiple files, for example:

```sql
SELECT *
FROM read_parquet('s3://⟨bucket_name⟩/*.parquet');
```

This query matches all files in the root of the bucket with the [Parquet extension]({% link docs/1.2/data/parquet/overview.md %}).

Several features for matching are supported, such as `*` to match any number of any character, `?` for any single character or `[0-9]` for a single character in a range of characters:

```sql
SELECT count(*) FROM read_parquet('s3://⟨bucket_name⟩/folder*/100?/t[0-9].parquet');
```

A useful feature when using globs is the `filename` option, which adds a column named `filename` that encodes the file that a particular row originated from:

```sql
SELECT *
FROM read_parquet('s3://⟨bucket_name⟩/*.parquet', filename = true);
```

This could for example result in:

| column_a | column_b | filename |
|:---|:---|:---|
| 1 | examplevalue1 | s3://bucket_name/file1.parquet |
| 2 | examplevalue1 | s3://bucket_name/file2.parquet |

### Hive Partitioning

DuckDB also offers support for the [Hive partitioning scheme]({% link docs/1.2/data/partitioning/hive_partitioning.md %}), which is available when using HTTP(S) and S3 endpoints.

## Writing

Writing to S3 uses the multipart upload API. This allows DuckDB to robustly upload files at high speed. Writing to S3 works for both CSV and Parquet:

```sql
COPY table_name TO 's3://⟨bucket_name⟩/⟨filename⟩.⟨extension⟩';
```

Partitioned copy to S3 also works:

```sql
COPY table TO 's3://⟨bucket_name⟩/partitioned' (
    FORMAT parquet,
    PARTITION_BY (⟨part_col_a⟩, ⟨part_col_b⟩)
);
```

An automatic check is performed for existing files/directories, which is currently quite conservative (and on S3 will add a bit of latency). To disable this check and force writing, an `OVERWRITE_OR_IGNORE` flag is added:

```sql
COPY table TO 's3://⟨bucket_name⟩/partitioned' (
    FORMAT parquet,
    PARTITION_BY (⟨part_col_a⟩, ⟨part_col_b⟩),
    OVERWRITE_OR_IGNORE true
);
```

The naming scheme of the written files looks like this:

```sql
s3://⟨your_bucket⟩/partitioned/part_col_a=⟨val⟩/part_col_b=⟨val⟩/data_⟨thread_number⟩.parquet
```

### Configuration

Some additional configuration options exist for the S3 upload, though the default values should suffice for most use cases.

| Name | Description |
|:---|:---|
| `s3_uploader_max_parts_per_file` | Used for part size calculation, see [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html) |
| `s3_uploader_max_filesize` | Used for part size calculation, see [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html) |
| `s3_uploader_thread_limit` | Maximum number of uploader threads |