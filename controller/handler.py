import json
import os
import sys
from utils import tokenizer


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
        self.cattle_species = ["lợn", "bò", "dê"]
        self.poultry_species = ["gà", "vịt"]
        self.agree_resp = ["đồng ý", "yes", "y", "dong y", "có", "co"]
        self.disagree_resp = ["không", "khong", "no"]

        # instance variables
        self.current_animal = ""
        self.current_species = ""

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

    def main_process(self):
        print("Bạn đã chọn sử dụng chức năng chẩn đoán bệnh thú y")
        print(
            "Đầu tiên, có thể cho tôi biết con vật mà bạn đang cần chẩn đoán bệnh? (VD: lợn, bò, gà...)"
        )
        self.current_animal = input().lower()
        self.current_species = self.check_species_db(self.current_animal)
        # warn user
        if self.current_species == "none":
            print(
                "Loài vật bạn cần chẩn đoán không có dữ liệu trong cơ sở dữ liệu chúng tôi, nhưng tôi sẽ cố hết sức để giúp đỡ trong khả năng của mình"
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
            if self.check_user_agree(u_in) == False:
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


class DiseasesInformation:
    pass


class MedicineInformation:
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

    def symptom_based_diagnose(self):
        pass

    def get_disease_information(self):
        print("2")

    def get_medicine_information(self):
        print("3")
