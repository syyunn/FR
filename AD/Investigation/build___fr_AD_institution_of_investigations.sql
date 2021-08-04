CREATE EXTENSION IF NOT EXISTS aws_commons CASCADE;

CREATE SCHEMA IF NOT EXISTS raw___fr;

DROP TABLE IF EXISTS raw___fr.ad_institution_of_investigations;

CREATE TABLE IF NOT EXISTS raw___fr.ad_institution_of_investigation (
    document_number text
    ,publication_date date
    ,product_name text
    ,hs_code text
    ,exporters text
    ,title text
    , primary key (document_number)
);

WITH s3_info AS (
    SELECT
        aws_commons.create_s3_uri ('wt-gc-m'
            , 'ds_chrono.csv'
            , 'ap-northeast-2') AS uri
        , aws_commons.create_aws_credentials ('AKIATHBCLRR3ZK5O6TGW'
            , 'f3icJzObixzX+04VHpakrlG+DZ7f8yTC1e92Atag'
            , NULL) AS cred
)
SELECT
    aws_s3.table_import_from_s3 ('raw___wto.ds_chrono' , '' , '(format csv, header)' , uri , cred)
FROM
    s3_info;