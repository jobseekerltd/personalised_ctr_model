from helpers import query_redshift
import os

query_redshift("""

         drop table if exists sandbox.jora_search_clicks
         create table sandbox.jora_search_clicks as
         (
         select s.user_id, s.job_title, case when c.job_id is not null then 1 else 0 end click_ind
               from jora.recent_job_stats s
               left join jora.recent_job_clicks c on c.tk = s.tk and c.job_id = s.job_id
               where s.site_id = 'nz'
               and s.created_at > '2016-11-01'
         );


         unload ('select * from sandbox.jora_search_clicks')
         to 's3://jora-data-science/personalised-ctr-model/jora-search-clicks.csv'
         CREDENTIALS 'aws_access_key_id={};aws_secret_access_key={}'
         DELIMITER '\t' ALLOWOVERWRITE PARALLEL OFF
         ;

""".format(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACESS_KEY']))

