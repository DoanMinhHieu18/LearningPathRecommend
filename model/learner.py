class Learner:
    def __init__(self, majors_list):
        self.learner_mssv = 2110162
        self.learner_english_level = 4
        self.learner_major = 5
        self.learn_summer_semester = True
        self.summer_semester_credit = 10
        self.number_of_free_elective_credit = 0
        # self.learner_mssv = input("Nhap mssv: ")
        # self.learner_english_level = input("Nhap trinh do tieng anh (Neu da hoan thanh: 1, Chua hoan thanh: 2): ")
        # if self.learner_english_level == 2:
        #     print("1. Anh van 1")
        #     print("2. Anh van 2")
        #     print("3. Anh van 3")
        #     print("4. Anh van 4")
        #     print("5. Chua hoan thanh bat ky anh van nao")
        #     self.learner_english_level = input("Tieng anh cua ban dang o trinh do nao (Vui long nhap theo dung so thu tu o tren): ")
        #     if self.learner_english_level == 5:
        #         self.learner_english_level = 1
        # else: 
        #     self.learner_english_level = 4
        # print("Danh sach cac chuyen nganh")
        # for major in majors_list:
        #     print(str(major.major_id) + ". " + major.major_name)
        # self.learner_major = input("Nhap chuyen nganh ma ban muon (Vui long nhap theo dung so thu tu o tren): ")
        # self.learn_summer_semester = input("Ban co muon hoc he khong (Co: 1, Khong: 0): ")
        # self.learn_summer_semester = True if self.learn_summer_semester == 1 else False