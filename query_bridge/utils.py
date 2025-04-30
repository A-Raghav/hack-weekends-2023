u1 = """Write a SQL query for transforming BENE_FIPS_STATE_CD into pst, and apply the following transformation:
Map
AR to Arkansas
CT to Connecticut
DC to District of Columbia
FL to Florida
GA to Georgia
HI to Hawaii
IA to Iowa. """
a1 = """case when bene_fips_state_cd= 'ar' then 'arkansas'
when bene_fips_state_cd = 'ct' then 'connecticut'
when bene_fips_state_cd = 'dc' then 'district of columbia'
when bene_fips_state_cd = 'fl' then 'florida'
when bene_fips_state_cd = 'ga' then 'georgia'
when bene_fips_state_cd = 'hi' then 'hawaii'
when bene_fips_state_cd = 'ia' then 'iowa'
end as pst"""

u2 = """Write a SQL query for transforming CLM_LINE_NUM into clid, and apply the following transformation:
No transformation. """
a2 = "clm_line_num as clid"

u3 = """Write a SQL query for transforming abc into xyz, and apply the following transformation:
None. """
a3 = "abc as xyz"

u4 = """Write a SQL query for transforming ALPHA_CODE into ftst, and apply the following transformation:
Coalesce with '' to remove any NULL values. """
a4 = "coalesce(alpha_code,'') as ftst"


u5 = """Write a SQL query for transforming CLM_FROM_DT into efdt, and apply the following transformation:
Date should not be blank, or '1000-01-01' or '9999-12-31. Convert values to date in YYYY-MM-DD format. """
a5 = """case when clm_from_dt not in ('','1000-01-01','9999-12-31') then (to_date(clm_from_dt,'yyyy-mm-dd')) end as efdt"""

u6 = """Write a SQL query for transforming CLM_LINE_PROD_REV_CTR_CD into rcc, and apply the following transformation:
Return an empty string if value is blank or '~'. Otherwise return the value of the column"""
a6 = """case when clm_line_prod_rev_ctr_cd in ('~','') then '' else clm_line_prod_rev_ctr_cd end as rcc"""

u7 = """Write a SQL query for transforming HCPCS_1_MDFR_CD into pm1, and apply the following transformation:
If value is not '~' then remove Null value else return empty string. """
a7 = """case when hcpcs_1_mdfr_cd in ('~','') then '' else coalesce(hcpcs_1_mdfr_cd,'') end as pm1"""

u8 = """Write a SQL query for transforming CLM_LINE_CVRD_PD_AMT into catp, and apply the following transformation:
Typecast to numeric data. Precision=18 and scale=2"""
a8 = """cast (clm_line_cvrd_pd_amt as numeric(18,2)) as catp"""

u9 = """Write a SQL query for transforming CUR_CLM_UNIQ_ID into cid, and apply the following transformation:
Trim any trailing or leading whitespaces. """
a9 = """trim(cur_clm_uniq_id) as cid"""

u10 = """Write a SQL query for transforming CLM_BILL_FAC_TYPE_CD, CLM_BILL_CLSFCTN_CD, CLM_BILL_FREQ_CD into bt, and apply the following transformation:
Concatenate the columns. """
a10 = """(clm_bill_fac_type_cd||clm_bill_clsfctn_cd||clm_bill_freq_cd) as bt"""

u11 = """Write a SQL query for transforming CLM_TYPE_CD, CLM_HIPPS_UNCOMPD_CARE_AMT into cuca, and apply the following transformation:
If CLM_TYPE_CD is not in ('10','20','30','40','50','60') then NULL, otherwise CLM_HIPPS_UNCOMPD_CARE_AMT. cast as decimal(18,2)"""
a11 = """case when clm_type_cd not in ('10','20','30','40','50','60') then cast (null as decimal(18,2)) else cast (clm_hipps_uncompd_care_amt as decimal(18,2)) end as cuca"""

messages = [
    {
        "role": "system",
        "content": "You are a helpful English to SQL translation assistant.",
    },
    {"role": "user", "content": u1},
    {"role": "assistant", "content": a1},
    {"role": "user", "content": u2},
    {"role": "assistant", "content": a2},
    {"role": "user", "content": u3},
    {"role": "assistant", "content": a3},
    {"role": "user", "content": u4},
    {"role": "assistant", "content": a4},
    {"role": "user", "content": u5},
    {"role": "assistant", "content": a5},
    {"role": "user", "content": u6},
    {"role": "assistant", "content": a6},
    {"role": "user", "content": u7},
    {"role": "assistant", "content": a7},
    {"role": "user", "content": u8},
    {"role": "assistant", "content": a8},
    {"role": "user", "content": u9},
    {"role": "assistant", "content": a9},
    {"role": "user", "content": u10},
    {"role": "assistant", "content": a10},
    {"role": "user", "content": u11},
    {"role": "assistant", "content": a11},
]
