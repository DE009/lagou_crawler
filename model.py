class Job(object):
    def __init__(self, job_name=None, salary=None, exp_req=None, edu_req=None, job_type=None, job_category=None,
                 labels=None, job_advantage=None, job_desc=None,
                 job_addr=None, company_id=None, category_id=None):
        self.job_name = job_name
        self.salary = salary
        self.exp_req = exp_req
        self.edu_req = edu_req
        self.job_type = job_type
        self.job_category = job_category
        self.labels = labels
        self.job_advantage = job_advantage
        self.job_desc = job_desc
        self.job_addr = job_addr
        self.company_id = company_id
        self.category_id = category_id


class Review(object):
    def __init__(self, iden_desc=None, interviewer=None, company_env=None, tags=None, review_content=None,job_id=None):
        self.iden_desc = iden_desc
        self.interviewer = interviewer
        self.company_env = company_env
        self.tags = tags
        self.review_content = review_content
        self.job_id = job_id


class Company(object):
    def __init__(self, company_name=None, bussiness_scope=None, company_stage=None, company_scale=None,
                 company_homepage=None, ):
        self.company_name = company_name
        self.bussiness_scope = bussiness_scope
        self.company_stage = company_stage
        self.company_scale = company_scale
        self.company_homepage = company_homepage

