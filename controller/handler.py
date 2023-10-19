import json
import os
import sys
from utils import tokenizer


class DiseasesDiagnosis:
    def __init__(self, cattle_db, poultry_db, generalized_db) -> None:
        self.cattle = cattle_db
        self.poultry = poultry_db
        self.ref_dict = generalized_db


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
        print("Bạn đã chọn sử dụng chức năng chẩn đoán bệnh thú y")

    def get_disease_information(self):
        print("2")

    def get_medicine_information(self):
        print("3")
