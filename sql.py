import pymysql


class SqlOperate():
    def __init__(self):
        self.conn = pymysql.Connect('localhost', user='root', password='123456', db='job_test')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()


class CategoryList(SqlOperate):
    def __init__(self, category):
        super().__init__()
        self.category = category

    def write_to_sql(self):
        job_title_urls = []
        self.cursor.execute(
            'create table IF NOT EXISTS category(id INT AUTO_INCREMENT PRIMARY KEY,category char(5),sub_category char(8),job_title varchar(20));')
        for data in self.category:
            self.cursor.execute("INSERT INTO category (category,sub_category,job_title) VALUES (%s, %s,%s)",
                                (data['category'], data['sub_category'], data['job_title']))
            self.cursor.execute('SELECT LAST_INSERT_ID()')
            inserted_id = self.cursor.fetchone()[0]
            #返回id和对应的urls内容（待改，不应该写这里的）
            row = {}
            row['category_id'] = inserted_id
            row['job_title_url'] = data['jor_title_url']
            job_title_urls.append(row)
        self.conn.commit()
        return job_title_urls


class JobDAL(SqlOperate):
    def __init__(self, job_model):
        super().__init__()
        self.model = job_model

    def write_to_sql(self):
        self.cursor.execute('create table IF NOT EXISTS job('
                            'id INT AUTO_INCREMENT PRIMARY KEY,'
                            'j_name varchar(30),'
                            'salary varchar(30),'
                            'exp_req varchar(10),'
                            'edu_req varchar(10),'
                            'job_type varchar(20),'
                            'job_category varchar(20),'
                            'labels text,'
                            'job_adv text,'
                            'job_desc text,'
                            'job_addr text,'
                            'compnay_id int,'
                            'category_id int'
                            ');')
        print('(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d,%d)' % (self.model.job_name,
                                                         self.model.salary,
                                                         self.model.exp_req,
                                                         self.model.edu_req,
                                                         self.model.job_type,
                                                         self.model.job_category,
                                                         self.model.labels,
                                                         self.model.job_advantage,
                                                         self.model.job_desc,
                                                         self.model.job_addr,
                                                         self.model.company_id,
                                                         self.model.category_id
                                                         ))
        self.cursor.execute(
            "INSERT INTO  job (j_name,salary,exp_req,edu_req,job_type,job_category,labels,job_adv,job_desc,job_addr,compnay_id,category_id) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (self.model.job_name,
             self.model.salary,
             self.model.exp_req,
             self.model.edu_req,
             self.model.job_type,
             self.model.job_category,
             self.model.labels,
             self.model.job_advantage,
             self.model.job_desc,
             self.model.job_addr,
             str(self.model.company_id),
             str(self.model.category_id)
             ))
        self.cursor.execute('SELECT LAST_INSERT_ID()')
        job_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return job_id


class ReviewDAL(SqlOperate):
    def __init__(self, review_model):
        super().__init__()
        self.model = review_model

    def write_to_sql(self):
        self.cursor.execute('create table IF NOT EXISTS review('
                            'id INT AUTO_INCREMENT PRIMARY KEY,'
                            'iden_desc int,'
                            'interviewer int,'
                            'company_env int ,'
                            'tags text,'
                            'content text,'
                            'job_id int'
                            ');')
        self.cursor.execute(
            "INSERT INTO review (iden_desc,interviewer,company_env,tags,content,job_id) VALUES (%s,%s,%s,%s,%s,%s)",
            (
                str(self.model.iden_desc),
                str(self.model.interviewer),
                str(self.model.company_env),
                self.model.tags,
                self.model.review_content,
                str(self.model.job_id),
            ))

        self.conn.commit()


class CompanyDAL(SqlOperate):
    def __init__(self, company_model):
        super().__init__()
        self.model = company_model

    def write_to_sql(self):
        self.cursor.execute('create table IF NOT EXISTS company('
                            'id INT AUTO_INCREMENT PRIMARY KEY,'
                            'c_name varchar(30),'
                            'b_scope varchar(40),'
                            'c_stage varchar(20),'
                            'c_scale varchar(20),'
                            'c_homepage text)'
                            ';')
        exist = self.cursor.execute("SELECT id from company where c_name=%s", self.model.company_name)
        if exist:
            return self.cursor.fetchone()[0]
        else:
            self.cursor.execute(
                "INSERT INTO company (c_name,b_scope,c_stage,c_scale,c_homepage) VALUES (%s, %s,%s,%s,%s)",
                (self.model.company_name,
                 self.model.bussiness_scope,
                 self.model.company_stage,
                 self.model.company_scale,
                 self.model.company_homepage))
            self.cursor.execute('SELECT LAST_INSERT_ID()')
            company_id = self.cursor.fetchone()[0]
            self.conn.commit()
            return company_id
