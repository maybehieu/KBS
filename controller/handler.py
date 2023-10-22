import json


def preprocess_animal_name(inp=""):
    convert = {
        "lợn": ["lon", "heo", "ỉn", "lợn"],
        "bò": ["bo", "bò"],
        "dê": ["de", "dê"],
        "trâu": ["trau", "nghé", "nghe", "trâu"],
        "gà": ["ga", "gà"],
        "ngan": ["ngan"],
        "vịt": ["vit", "vịt"],
    }
    for w, c in convert:
        if inp in c:
            return w
    return inp


def get_similar_animals(inp=""):
    similar = {
        "lợn": [],
        "bò": ["trâu"],
        "dê": [],
        "trâu": ["bò"],
        "gà": ["gà"],
        "ngan": ["vịt"],
        "vịt": ["ngan"],
    }
    return similar[inp]


class Disease:
    def __init__(self, j = {}, index=-1) -> None:
        self.name = j['name']
        self.species = j['species']
        self.description = j['description']
        self.causes = j['causes']
        self.environment_factors = j['evnfactors']
        self.symptoms = j['symptoms']
        self.treatments = j['treatments']
        self.prevention = j['prevention']

        self.index = index

    def get_name(self):
        return self.name

    def get_species(self):
        return self.species

    def get_description(self):
        return self.description

    def get_causes(self):
        return self.causes

    def get_environment_factors(self):
        return self.environment_factors

    def get_symptoms(self):
        return self.symptoms

    def get_treatments(self):
        return self.treatments

    def get_prevention(self):
        return self.prevention
    
    def get_index(self):
        return self.index
    
    def print_basic(self):
        print(f'==== Thông tin bệnh {self.name} ====')
        print(f'Tổng quan bệnh: {self.description}')
        print(f'- Các loài có thể bị nhiễm: {self.species}')
        print(f'Số thứ tự: {self.index}')
        # có thể in thêm các triệu chứng nổi bật, sẽ code thêm khi database có thêm phần trọng số
    


class DiseasesDiagnosis:
    def __init__(
        self, cattle_db, poultry_db, r_cattle_db, r_poultry_db, generalized_db
    ) -> None:
        # global variables
        self.cattle = cattle_db
        self.poultry = poultry_db
        self.r_cattle = r_cattle_db
        self.r_poultry = r_poultry_db
        self.ref_dict = generalized_db
        self.cattle_species = ["lợn", "bò", "dê", "trâu"]
        self.poultry_species = ["gà", "vịt", "ngan"]
        self.agree_resp = ["đồng ý", "yes", "y", "dong y", "có", "co"]
        self.disagree_resp = ["không", "khong", "no", "kết thúc", "ket thuc"]

        # instance variables
        self.current_animal = ""
        self.current_species = ""

    def main_process(self):
        print("Bạn đã chọn sử dụng chức năng chẩn đoán bệnh thú y")
        print(
            "Đầu tiên, có thể cho tôi biết con vật mà bạn đang cần chẩn đoán bệnh? (VD: lợn, bò, gà...)"
        )
        self.current_animal = input().lower()
        self.current_animal = preprocess_animal_name(self.current_animal)
        self.current_species = self.check_species_db(self.current_animal)
        # warn user
        if self.current_species == "none":
            print(
                "Loài vật bạn cần chẩn đoán không có dữ liệu trong cơ sở dữ liệu chúng tôi, nhưng tôi sẽ cố hết sức để giúp đỡ bạn trong khả năng của mình"
            )
            u_in = input("Bạn có muốn tiếp tục? ")
            # exit if needed
            if self.check_user_agree(u_in) == None:
                if not self.check_user_agree(
                    input(
                        "Tôi không hiểu câu trả lời của bạn, hãy phản hồi theo dạng có/không: "
                    )
                ):
                    print("Xin cảm ơn!")
                    return
            elif not self.check_user_agree(u_in):
                print("Xin cảm ơn!")
                return
        # continue
        print(
            f'Xác định thông tin ban đầu của con vật: {self.current_animal.capitalize()}, là {"Gia súc" if self.current_species == "cattle" else "Gia cầm"}'
        )
        # thực hiện hỏi yếu tố môi trường

        # thực hiện hỏi triệu chứng

        # thực hiện tính toán tìm case

        # tiền xử lý

    def check_species_db(self, inp=""):
        if inp in self.cattle_species:
            return "cattle"
        if inp in self.poultry_species:
            return "poultry"
        return "none"

    def check_user_agree(self, inp=""):
        if inp in self.agree_resp:
            return True
        if any(word in inp for word in self.agree_resp):
            return True
        if inp in self.disagree_resp:
            return False
        if any(word in inp for word in self.disagree_resp):
            return False
        return None


class DiseasesInformation:
    def __init__(
        self, cattle_db, poultry_db, r_cattle_db, r_poultry_db, generalized_db
    ) -> None:
        # global variables
        self.cattle = cattle_db
        self.poultry = poultry_db
        self.r_cattle = r_cattle_db
        self.r_poultry = r_poultry_db
        self.ref_dict = generalized_db
        self.agree_resp = ["đồng ý", "yes", "y", "dong y", "có", "co"]
        self.disagree_resp = ["không", "khong", "no", "kết thúc", "ket thuc"]
        self.cattle_species = ["lợn", "bò", "dê", "trâu"]
        self.poultry_species = ["gà", "vịt", "ngan"]

        # instance variables
        self.current_animal = ""
        self.current_species = ""
        self.current_avail_diseases = []
        self.current_similar_animals = []
        self.current_pick_disease = None

    def main_process(self):
        print("Bạn đã chọn sử dụng chức năng tìm kiếm thông tin về bệnh thú y")
        print(
            "Đầu tiên, bạn có thể cho tôi biết bệnh mà bạn đang tìm kiếm có liên quan để con vật nào không?"
        )
        self.current_animal = input().lower()
        # tiền xử lý tên con vật
        self.current_animal = preprocess_animal_name(self.current_animal)
        # kiểm tra tên con vật trong cơ sở dữ liệu
        self.current_species = self.check_species_db(self.current_animal)
        if self.current_species == "none":
            self.current_similar_animals = get_similar_animals(self.current_animal)
            print(
                "Con vật mà bạn đang tìm kiếm không nằm trong cơ sở dữ liệu của tôi",
                sep="",
            )
            if len(self.current_similar_animals) == 0:
                print(
                    "Trong cơ sở dữ liệu của tôi hiện đang chưa được cập nhật các dữ liệu liên quan đến con vật của bạn, tôi sẽ đưa bạn về menu lựa chọn, xin cảm ơn!"
                )
                return
            elif len(self.current_similar_animals != 0):
                print(
                    f'Trong cơ sở dữ liệu của tôi hiện đang có những con vật tương tự với 
                    {self.current_animal.capitalize()} như {", ".join(self.current_similar_animals)}, bạn có muốn tiếp tục không?'
                )
                u_in = input()
                if self.check_user_agree(u_in) == None:
                    if not self.check_user_agree(
                        input(
                            "Tôi không hiểu câu trả lời của bạn, hãy phản hồi theo dạng có/không: "
                        )
                    ):
                        print("Xin cảm ơn!")
                        return
                elif not self.check_user_agree(u_in):
                    print("Xin cảm ơn!")
                    return
            self.current_animal = ''
        # tìm bệnh
        self.current_avail_diseases = self.get_avail_diseases()
        self.current_avail_diseases = [Disease(d, index) for index, d in enumerate(self.current_avail_diseases)]
        # trả về thông tin cho người dùng
        # # thông tin cơ bản
        print('Dưới đây là danh sách các bệnh liên quan đến con vật mà bạn yêu cầu:')
        for ds in self.current_avail_diseases: ds.print_basic()
        # tiến hành hỏi-đáp
        # chọn một loại bệnh
        while True:
            u_in = input('Hãy nhập số thứ tự của bệnh bạn muốn tìm hiểu, hoặc nhập "kết thúc" nếu bạn muốn dừng phiên hoạt động: ')
            # check stop
            if u_in == "kết thúc":
                break
            # check index
            while True:
                if int(u_in) > len(self.current_avail_diseases) or int(u_in) < len(self.current_avail_diseases):
                    u_in = input('Vui lòng chỉ nhập những số thứ tự tôi đã liệt kê ở trên :(: )')
                    continue
                break
            # khoá bệnh người dùng chọn
            self.current_pick_disease = self.current_avail_diseases[int(u_in)]
            print(f'Bạn đã chọn bệnh {self.current_pick_disease.get_name()}, để chọn bệnh khác, vui lòng nhập "kết thúc"')
            print('Lưu ý rằng tôi không quá giỏi khi phân tích ngữ nghĩa, vì vậy sử dụng các từ gợi ý tôi đưa ra có thể giúp tôi trợ giúp bạn dễ hơn')
            # hỏi đáp từng câu
            current_context = ''
            while True:
                u_in = input('Bạn muốn biết thông tin gì về bệnh? (nguyên nhân, triệu chứng, cách điều trị, cách phòng bệnh) ')
                # this is where i left
                pass


        

    def get_avail_diseases(self):
        if self.current_species == 'cattle':
            return self.find_diseases_animal_based(self.current_animal, self.r_cattle)
        if self.current_species == 'poultry':
            return self.find_diseases_animal_based(self.current_animal, self.r_poultry)
        return self.find_diseases_animal_based(self.current_similar_animals, self.r_cattle + self.r_poultry)

    # iterate through every diseases
    def find_diseases_animal_based(self, a_names = [''], diseases = []):
        ret = []
        for disease in diseases:
            for name in a_names:
                if name.lower() in disease['species']: ret.append(disease)
        return list(set(ret))
    
    def check_user_agree(self, inp=""):
        if inp in self.agree_resp:
            return True
        if any(word in inp for word in self.agree_resp):
            return True
        if inp in self.disagree_resp:
            return False
        if any(word in inp for word in self.disagree_resp):
            return False
        return None

    def check_species_db(self, inp=""):
        if inp in self.cattle_species:
            return "cattle"
        if inp in self.poultry_species:
            return "poultry"
        return "none"


class MedicineInformation:
    def __init__(self, medic_db) -> None:
        self.medicine_db = medic_db

    def main_process(self):
        print("Bạn đã chọn sử dụng chức năng tìm kiếm thông tin thuốc thú y")
        pass


class ChatbotController:
    def __init__(self) -> None:
        with open(r"database\cattle.json", "r", encoding="utf8") as f:
            self.cattle_database = json.loads(f.read())
        with open(r"database\poultry.json", "r", encoding="utf8") as f:
            self.poultry_database = json.loads(f.read())
        with open(r"database\medicine.json", "r", encoding="utf8") as f:
            self.medicine_database = json.loads(f.read())
        with open(r"database\convert.json", "r", encoding="utf8") as f:
            self.generalized_database = json.loads(f.read())
        with open(r"database\r_cattle.json", "r", encoding="utf8") as f:
            self.r_cattle_database = json.loads(f.read())
        with open(r"database\r_poultry.json", "r", encoding="utf8") as f:
            self.r_poultry_database = json.loads(f.read())
        # options for user
        self.convo_options = [
            "1. Chẩn đoán bệnh thú y dựa theo triệu chứng",
            "2. Tìm kiếm thông tin về bệnh thú y",
            "3. Tìm kiếm thông tin về thuốc thú y",
        ]

    def main_process(self):
        # loop every process until special condition (user asks to stop)
        while True:
            self.print_start_convo()
            u_input = input()
            u_input = self.check_master_convo(u_input)
            if u_input == 1:
                self.symptom_based_diagnose()
            elif u_input == 2:
                self.get_disease_information()
            elif u_input == 3:
                self.get_medicine_information()
            elif u_input == 0:
                self.print_end_convo()
                break

        print("Dừng hệ thống.")

    def print_start_convo(self):
        print(
            "Xin chào bạn đến với hệ thống chatbot tư vấn khám chữa bệnh thú y. Vui lòng chọn một lựa chọn phía dưới"
        )
        print("\n".join(self.convo_options))

    def print_end_convo(self):
        print("Cảm ơn bạn đã sử dụng hệ thống, hẹn gặp lại!")

    def check_master_convo(self, user_input=""):
        end_convo_words = ["kết thúc", "ket thuc", "thoat", "end", "quit", "exit"]
        try:
            opt = int(user_input)
            return opt
        except:
            if user_input.lower() in end_convo_words:
                return 0

    def symptom_based_diagnose(self):
        pass

    def get_disease_information(self):
        print("2")

    def get_medicine_information(self):
        print("3")
