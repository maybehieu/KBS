import json
import math

from controller.utils import tokenizer


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
    for key in convert:
        if inp in convert[key]:
            return key
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


def string_preprocess(s=""):
    s = s.lower()
    return tokenizer(s)


# tạo một dict với keys là các từ thuộc tập tổng các từ (toàn bộ doc) với value là số lần xuất hiện trong câu đầu vào
def make_word_dict(all_word, doc=[]):
    wordDict = dict.fromkeys(all_word, 0)
    for word in doc:
        try:
            wordDict[word] += 1
        except:
            pass
    return wordDict


# tính toán giá trị term-frequency
# tf(từ) = số lần xuất hiện của từ / tổng số từ (trong câu)
def compute_tf(wordDict, doc=[]):
    tfDict = {}
    wordNum = len(doc)
    for word, count in wordDict.items():
        tfDict[word] = count / float(wordNum)
    return tfDict


# tính toán giá trị inverse document frequency
# idf(từ) = log(số lượng văn bản / số lượng văn bản có chứa từ đó)
def compute_idf(docList=[]):
    idfDict = {}
    N = len(docList)

    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for word, val in idfDict.items():
        count = 0
        for _dict in docList:
            try:
                if _dict[word] > 0:
                    count += 1
            except:
                pass
        if count == 0:
            count = 1
        idfDict[word] = math.log(N / float(count))

    return idfDict


# tính toán giá trị tfidf
# tfidf(từ) = tf * idf
def compute_tfidf(tf, idf):
    tfidf = {}
    for word, val in tf.items():
        tfidf[word] = val * idf[word]
    return tfidf


def cosine_similarity(tfidf_vector1, tfidf_vector2):
    # tính tích vô hướng của 2 vector
    dot_product = sum(
        tfidf_vector1[term] * tfidf_vector2[term]
        for term in tfidf_vector1
        if term in tfidf_vector2
    )

    # tính toán chuẩn euclidean của 2 vector
    magnitude1 = math.sqrt(sum(tfidf_vector1[term] ** 2 for term in tfidf_vector1))
    magnitude2 = math.sqrt(sum(tfidf_vector2[term] ** 2 for term in tfidf_vector2))

    # tính toán độ tương đồng cosine
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    else:
        return dot_product / (magnitude1 * magnitude2)


class Disease:
    def __init__(
        self,
        j={
            "name": "Holder",
            "species": [],
            "description": "",
            "causes": [],
            "envfactors": [],
            "symptoms": [],
            "treatments": [],
            "prevention": [],
        },
        index=-1,
        w={"": {"": 0.0}},
    ) -> None:
        self.name = j["name"]
        self.species = j["species"]
        self.description = j["description"]
        self.causes = j["causes"]
        self.treatments = j["treatments"]
        self.prevention = j["prevention"]
        self.weight = {}
        try:
            self.weight = w[self.name]
        except:
            print(f"Không tìm thấy trọng số của bệnh {self.name}")
        # will be redefined
        self.environment_factors = j["envfactors"]
        self.symptoms = j["symptoms"]

        self.index = index

        self.all_envsym = []
        # self.all_envsym = self.environment_factors + self.symptoms
        self.all_envsym = [[i] for i in self.environment_factors] + self.symptoms

    def init_temp(self, env=[], sym=[]):
        self.environment_factors = env
        self.symptoms = sym
        self.all_envsym = self.environment_factors + self.symptoms

    def update_temp(self, envsym=[]):
        self.all_envsym.extend(envsym)

    def get_sym_from_key(self, key=""):
        for _sym in self.symptoms:
            if _sym[0] == key:
                return _sym
        return None

    def get_envsym_not_appear_weight_based(self, asked=[[""]]):
        ret = []
        for key in self.weight:
            sym_env = self.get_sym_from_key(key)
            if sym_env is not None and sym_env not in asked:
                ret.append((key, self.weight[key]))
            elif sym_env is None and [key] not in asked:
                ret.append((key, self.weight[key]))
        ret = sorted(ret, key=lambda x: x[1], reverse=True)
        if len(ret) > 0:
            if self.get_sym_from_key(ret[0][0]) is not None:
                return self.get_sym_from_key(ret[0][0])
        return [ret[0][0]] if len(ret) > 0 else "none"

    def process_symptoms(self):
        pass

    def process_envfacs(self):
        pass

    def print_species(self):
        print(self.species)

    def print_description(self):
        print(self.description)

    def print_causes(self):
        print(self.causes)

    def print_environment_factors(self):
        print(self.environment_factors)

    def print_symptoms(self):
        print(self.symptoms)

    def print_treatments(self):
        print(self.treatments)

    def print_prevention(self):
        print(self.prevention)

    def get_index(self):
        return self.index

    def print_basic(self):
        print(f"==== Thông tin bệnh {self.name} ====")
        print(f"Tổng quan bệnh: {self.description}")
        print(f"- Các loài có thể bị nhiễm: {self.species}")
        print(f"Số thứ tự: {self.index}")
        # có thể in thêm các triệu chứng nổi bật, sẽ code thêm khi database có thêm phần trọng số

    def print_all(self):
        print(self.name + " all")


class ChatbotController:
    def __init__(self) -> None:
        print("Đang khởi tạo hệ thống...")
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
        with open(r"database\weights.json", "r", encoding="utf8") as f:
            self.weights = json.loads(f.read())
        # options for user
        self.convo_options = [
            "1. Chẩn đoán bệnh thú y dựa theo triệu chứng",
            "2. Tìm kiếm thông tin về bệnh thú y",
            "3. Tìm kiếm thông tin về thuốc thú y",
        ]

        # init logic controller
        self.diagnose = DiseasesDiagnosis(
            self.cattle_database,
            self.poultry_database,
            self.r_cattle_database,
            self.r_poultry_database,
            self.generalized_database,
            self.weights,
        )
        self.disease = DiseasesInformation(
            self.cattle_database,
            self.poultry_database,
            self.r_cattle_database,
            self.r_poultry_database,
            self.generalized_database,
        )
        # self.medicine = MedicineInformation()

    def main_process(self):
        # loop every process until special condition (user asks to stop)
        while True:
            self.print_start_convo()
            u_input = input()
            u_input = self.check_master_convo(u_input)
            if u_input == 1:
                # self.symptom_based_diagnose()
                self.diagnose.main_process()
            elif u_input == 2:
                # self.get_disease_information()
                self.disease.main_process()
            elif u_input == 3:
                # self.get_medicine_information()
                self.medicine.main_process()
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


class DiseasesDiagnosis:
    def __init__(
        self,
        cattle_db,
        poultry_db,
        r_cattle_db,
        r_poultry_db,
        generalized_db,
        a_weights,
    ) -> None:
        # global variables
        self.cattle = [
            Disease(j, index, a_weights) for index, j in enumerate(cattle_db)
        ]
        self.poultry = [
            Disease(j, index, a_weights) for index, j in enumerate(poultry_db)
        ]
        self.r_cattle = r_cattle_db
        self.r_poultry = r_poultry_db
        self.ref_dict = generalized_db
        self.cattle_species = ["lợn", "bò", "dê", "trâu"]
        self.poultry_species = ["gà", "vịt", "ngan"]
        self.agree_resp = ["đồng ý", "dong y", "có", "co"]
        self.disagree_resp = ["không", "khong", "kết thúc", "ket thuc", "dừng"]
        self.neutral_words = [
            "bình thường",
            "ổn định",
            "trung bình",
            "lý tưởng",
            "rộng rãi",
            "thoáng mát",
            "sạch sẽ",
        ]
        self.cbr_threshold = 0.7
        self.match_threshold = 0.9

        self.all_symenv = []
        for obj in self.ref_dict:
            self.all_symenv.extend(obj["distinct"])
        self.proc_all_symenv = [string_preprocess(sent) for sent in self.all_symenv]

        # instance variables
        self.current_animal = ""
        self.current_species = ""
        self.current_symptoms = []
        self.current_envfacs = []
        self.current_envsyms = []
        self.diagnosed_disease = None

        print("Core Diagnose done")

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
        # chẩn đoán bệnh
        self.diagnosed_disease = self.diagnose()
        # tương tác xử lý thông tin cho người dùng
        self.support_user()

    def support_user(self):
        print(
            f'Xác định được bệnh mà con vật của bạn đang gặp phải là bệnh "{self.diagnosed_disease.name}"\n'
            f"Các thông tin cơ bản của bệnh bao gồm:\n"
        )
        self.diagnosed_disease.print_basic()
        print(
            "Các chức năng khả dụng hiện tại:\n"
            "1. Nêu nguyên nhân bệnh\n"
            "2. Nêu các triệu chứng của bệnh\n"
            "3. Nêu cách phòng bệnh\n"
            "4. Nêu cách chữa bệnh\n"
            "0. Kết thúc trò chuyện\n"
        )
        opts = [0, 1, 2, 3, 4]
        state = False
        while True:
            u_in = input("Vui lòng nhập lựa chọn của bạn: ")
            while True:
                try:
                    u_in = int(u_in)
                    if u_in not in opts:
                        print("Vui lòng chỉ chọn các lựa chọn phía trên")
                        break
                except:
                    print("Vui lòng sử dụng số khi bạn lựa chọn chức năng muốn sử dụng")
                    break
            if not state:
                continue

    def diagnose(self):
        print(
            "Tôi sẽ bắt đầu thực hiện việc tìm hiểu thông tin để chẩn đoán bệnh trên con vật bạn đang chọn. Lưu ý rằng với các triệu chứng, yếu tố khác nhau, "
            + 'bạn hãy ngăn cách chúng bằng dấu ";", và hãy chỉ đưa ra những triệu chứng, yếu tố được yêu cầu một cách ngắn gọn, trong mỗi câu trả lời để kết quả đạt được là tốt nhất'
        )

        # thực hiện hỏi yếu tố môi trường
        print(
            f"Đầu tiên hãy bắt đầu với các yếu tố môi trường xung quanh vật nuôi của bạn"
        )
        self.get_envsym(
            f"Thời tiết tại chỗ bạn đang như thế nào? (bình thường, thất thường, thay đổi,...)"
        )
        self.get_envsym(
            "Nhiệt độ xung quanh khu vực chuồng của vật nuôi trong thời gian gần nhất như thế nào? (cao, thấp, thất thường,...)"
        )
        self.get_envsym(
            "Điều kiện chuồng nuôi của con vật hiện tại như thế nào? (sạch sẽ, bẩn, chật hẹp, ...)"
        )
        self.get_envsym(
            "Thức ăn của con vật có đảm bảo không? (uống nước ao tù, thức ăn để lâu, thức ăn công nghiệp, ...)"
        )
        # thực hiện hỏi triệu chứng
        self.get_envsym(
            "Con vật có dấu hiệu uể oải, khác so với ngày thường không? (bình thường, năng động, uể oải, ủ rũ, ...)",
            mode="sym",
        )
        self.get_envsym(
            "Con vật có dấu hiệu bất thường gì có thể nhìn được bằng mắt thường không? (chấm đỏ trên da, mắt đỏ, sổ mũi, ...)",
            mode="sym",
        )
        self.get_envsym(
            "Con vật có ăn uống như bình thường không? (chán ăn, ăn bình thường, ...)",
            mode="sym",
        )
        self.get_envsym(
            "Con vật có triệu chứng sốt không? (không, sốt nhẹ, sốt cao, sốt li bì, ...)",
            mode="sym",
        )
        # thực hiện tính toán tìm case
        temp_disease = Disease()
        temp_disease.init_temp(self.current_envfacs, self.current_symptoms)
        if self.current_species != "none":
            comparison_diseases = (
                self.cattle if self.current_species == "cattle" else self.poultry
            )
        else:
            comparison_diseases = {**self.cattle, **self.poultry}
        disease_similarities = (
            []
        )  # format: ((bệnh đang được chẩn đoán, bệnh đã có trong hệ tri thức), độ tương đồng)
        # so sánh với các case đã có sẵn trong hệ tri thức
        for d in comparison_diseases:
            disease_similarities.append(
                ((temp_disease, d), self.calculate_cbr(temp_disease, d))
            )
        disease_similarities = sorted(
            disease_similarities, key=lambda x: x[1], reverse=True
        )
        print("debug, thông tin sử dụng trong bệnh")
        print(temp_disease.all_envsym)
        print("debug, danh sách các bệnh và độ tương đồng: ")
        for d in disease_similarities:
            print(f"query: {d[0][0].name}, db: {d[0][1].name}, sim: {d[1]}")
        # chọn ra n case có độ tương đồng cao nhất, thực hiện hỏi thêm triệu chứng nếu cần
        top = disease_similarities[:5]
        if top[0][1] >= self.match_threshold:
            return top[0][0][1]
        # chẩn đoán sâu
        top = [item[0][1] for item in top]
        return self.further_diagnose(diag=temp_disease, potential=top)

    def further_diagnose(self, diag=Disease(), potential=[Disease()]):
        # thực hiện hỏi một triệu chứng có trọng số cao nhất ở mỗi bệnh, lặp lại cho đến khi độ tương đồng với bệnh chẩn đoán vượt ngưỡng
        asked = []
        cnt = 0
        sim = []
        while cnt < 2:
            print("debug, thông tin trong bệnh đang được chẩn đoán")
            print(diag.all_envsym)
            print("debug, thông tin đã được hỏi")
            print(asked)
            sim = []
            # tìm triệu chứng có trọng số cao nhất trong mỗi bệnh
            for disease in potential:
                _envsym = disease.get_envsym_not_appear_weight_based(asked)
                if _envsym == "none":
                    continue
                # if _envsym in asked or _envsym[0] in diag.all_envsym:
                if _envsym in asked:
                    continue
                # thực hiện hỏi
                if self.get_yesno_envsym(_envsym):
                    diag.all_envsym.append(_envsym[0])
                asked.append(_envsym)
            # tính toán lại độ tương đồng
            for disease in potential:
                sim.append(((diag, disease), self.calculate_cbr(diag, disease)))
            sim = sorted(sim, key=lambda x: x[1], reverse=True)
            print("debug, danh sách các bệnh và độ tương đồng: ")
            for d in sim:
                print(f"query: {d[0][0].name}, db: {d[0][1].name}, sim: {d[1]}")
            if sim[0][1] > self.match_threshold:
                return sim[0][0][1]
            cnt += 1
        # trả về case có giá trị tương đồng cao nhất
        return sim[0][0][1]

    def get_envsym(self, msg="", mode="env"):
        _in = input(msg + ": ")
        # tách dữ liệu đầu vào nếu cần
        _in = _in.split(";")
        for data in _in:
            _out, _data = self.find_symenv_tfidf_based(data)
            # tiền xử lý dữ liệu đầu vào
            # KHÔNG bỏ qua triệu chứng nếu trong câu chứa cả từ phủ định và tích cực (không + sạch sẽ -> không sạch sẽ)
            if any(neutral in _data for neutral in self.neutral_words) and any(
                negative in _data for negative in self.disagree_resp
            ):
                print(
                    f"debug: xuất hiện case nega-neutral, double check dữ liệu: {data} -> {_data}"
                )
                pass
            # bỏ qua triệu chứng nếu xuất hiện các từ 'trung hoà' trong dữ liệu nhập vào của người dùng
            elif any(neutral in _data for neutral in self.neutral_words):
                print(f"debug: xuất hiện neutral trong {data}, bỏ qua triệu chứng")
                continue
            # bỏ qua triệu chứng nếu xuất hiện từ 'không' trong dữ liệu nhập vào (không sốt)
            elif any(negative in _data for negative in self.disagree_resp):
                print(f"debug: xuất hiện negative trong {data}, bỏ qua triệu chứng")
                continue
            print(f'debug: người dùng nhập "{data}", hệ thống trả về "{_out}"')
            if _out == "none":
                print(
                    f"Hệ thống không thể nhận dạng được câu trả lời bạn đưa ra ({data}), vui lòng thử lại"
                )
                return self.get_envsym(msg, mode)

            # lưu kết quả
            if mode == "env":
                self.current_envfacs.append(_out)
            elif mode == "sym":
                self.current_symptoms.append(_out)
            self.current_envsyms.append(_out)

    def get_yesno_envsym(self, envsym=[]):
        # in lưu ý
        ques = ""
        sup = ""
        print("Đây là câu hỏi trả lời dạng có/ không")
        if len(envsym) > 1:
            ques = envsym[0]
            sup = envsym[1]
            _in = input(
                f'Con vật của bạn có triệu chứng "{ques}" không? ("{ques}" thường có các biểu hiện như {sup})\n'
            )
        else:
            ques = envsym[0]
            _in = input(f'Con vật của bạn có triệu chứng "{ques}" không? ')
        return self.check_user_agree(_in)

    def get_timebased_envsym(self, msg=""):
        # in lưu ý
        print(
            'Đây là câu hỏi về thời gian, vui lòng trả lời theo định dạng "{ngày}" hoặc "{ngày}-{ngày}. VD: từ 2 đến 3 ngày -> 2-3"'
        )
        _in = input(msg + ": ")
        _in = _in.split("-")

    # trả về độ tương đồng giữa case hiện tại và case có trong hệ tri thức
    def calculate_cbr(self, query=Disease(), compare=Disease()):
        dsum = 0.0
        _sum = 0.0
        for key in compare.weight:
            try:
                if key in query.all_envsym and key in compare.weight:
                    dsum += float(compare.weight[key])
                _sum += float(compare.weight[key])
            except:
                pass
                # print(key)
                # print(query.all_envsym, compare.all_envsym, compare.weight)
        if _sum == 0.0:
            return 0.0
        return dsum / _sum

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

    def find_symenv_tfidf_based(self, inp):
        lst = self.all_symenv
        _lst = self.proc_all_symenv
        objs = self.ref_dict

        # lấy toàn bộ các từ
        total = [word for sent in _lst for word in sent]
        _inp = string_preprocess(inp)
        total.extend(_inp)

        # tạo ra một list các từ độc nhất
        total = list(set(total))
        a_worddict = [make_word_dict(total, sent) for sent in _lst]
        q_worddict = make_word_dict(total, _inp)

        # tính toán tf
        a_tfs = []
        for idx in range(len(lst)):
            a_tfs.append(compute_tf(a_worddict[idx], _lst[idx]))
        tf = compute_tf(q_worddict, _inp)

        # tính toán idf
        idfs = compute_idf(a_tfs + [tf])

        # tính toán tfidf
        a_tfidfs = []
        for idx in range(len(lst)):
            a_tfidfs.append(compute_tfidf(a_tfs[idx], idfs))
        q_tfidf = compute_tfidf(tf, idfs)

        # tính toán tương đồng cosine giữa câu đầu vào và các câu có trong hệ thống
        sims = [cosine_similarity(q_tfidf, tfidf) for tfidf in a_tfidfs]

        # # debug
        # for sentence, score in zip(lst, sims):
        #     print(f'độ tương đồng giữa query và {sentence}: {score}')

        # sắp xếp theo độ tương đồng cao nhất
        sort = sorted(zip(lst, sims), key=lambda x: x[1], reverse=True)
        lst, sims = zip(*sort)

        # debug
        # print('sau sắp xếp')
        # for sentence, score in zip(lst, sims):
        #     print(f'độ tương đồng giữa query và {sentence}: {score}')

        # lấy ra 5 câu có độ tương đồng cao nhất
        # top = lst[:5]
        top, top_score = [], []
        # loại bỏ các phần tử có độ tương đồng bằng 0
        for string, score in sort:
            if score == 1.0:
                top.append(string)
                top_score.append(score)
            if score > 0.0:
                top.append(string)
                top_score.append(score)
                if len(top) == 5:
                    break
        if len(top) == 0:
            return "none", _inp

        # debug
        for sentence, score in zip(top, top_score):
            print(f"độ tương đồng giữa query và {sentence}: {score}")

        max_match_count = 0
        return_symenv = ""
        for obj in objs:
            match_count = len([i for i in top if i in obj["distinct"]])
            if match_count > max_match_count:
                max_match_count = match_count
                return_symenv = obj["general"]

        return return_symenv, _inp

    def find_symenv_string_based(self, inp=""):
        lst = self.all_symenv
        _lst = self.proc_all_symenv
        objs = self.ref_dict

        for string in lst:
            if inp.lower().strip() == string:
                for obj in objs:
                    if string in obj["distinct"]:
                        return obj["general"]

        return "none"


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

        print("Core Info done")

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
                    f"Trong cơ sở dữ liệu của tôi hiện đang có những con vật tương tự với "
                    + f'{self.current_animal.capitalize()} như {", ".join(self.current_similar_animals)}, bạn có muốn tiếp tục không?'
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
            self.current_animal = ""
        # tìm bệnh
        self.current_avail_diseases = self.get_avail_diseases()
        self.current_avail_diseases = [
            Disease(d, index) for index, d in enumerate(self.current_avail_diseases)
        ]
        # trả về thông tin cho người dùng
        # # thông tin cơ bản
        print("Dưới đây là danh sách các bệnh liên quan đến con vật mà bạn yêu cầu:")
        for ds in self.current_avail_diseases:
            ds.print_basic()
        # tiến hành hỏi-đáp
        # chọn một loại bệnh
        while True:
            u_in = input(
                'Hãy nhập số thứ tự của bệnh bạn muốn tìm hiểu, hoặc nhập "kết thúc" nếu bạn muốn dừng phiên hoạt động: '
            )
            # check stop
            if u_in == "kết thúc":
                break
            # check index
            while True:
                if int(u_in) > len(self.current_avail_diseases) or int(u_in) < len(
                    self.current_avail_diseases
                ):
                    u_in = input(
                        "Vui lòng chỉ nhập những số thứ tự tôi đã liệt kê ở trên :(: )"
                    )
                    continue
                break
            # khoá bệnh người dùng chọn
            self.current_pick_disease = self.current_avail_diseases[int(u_in)]
            print(
                f'Bạn đã chọn bệnh {self.current_pick_disease.name}, để chọn bệnh khác, vui lòng nhập "kết thúc"'
            )
            print(
                "Lưu ý rằng tôi không quá giỏi khi phân tích ngữ nghĩa, vì vậy sử dụng các từ gợi ý tôi đưa ra có thể giúp tôi trợ giúp bạn dễ hơn"
            )
            # hỏi đáp từng câu
            current_context = ""
            while True:
                # cần (?) preprocess tách ngữ cảnh
                u_in = input(
                    "Bạn muốn biết thông tin gì về bệnh? (nguyên nhân, mô tả, triệu chứng, cách điều trị, cách phòng bệnh, toàn bộ) "
                )
                if "nguyên nhân" in u_in.lower().strip():
                    print(
                        f"Dưới đây là các nguyên nhân gây nên bệnh {self.current_pick_disease.name}"
                    )
                    self.current_pick_disease.print_causes()
                if "mô tả" in u_in.lower().strip():
                    print(
                        f"Dưới đây là phần mô tả của bệnh {self.current_pick_disease.name}"
                    )
                    self.current_pick_disease.print_description()
                if "triệu chứng" in u_in.lower().strip():
                    print(
                        f"Dưới đây là các triệu chứng của bệnh {self.current_pick_disease.name}"
                    )
                    self.current_pick_disease.print_symptoms()
                if "điều trị" in u_in.lower().strip():
                    print(
                        f"Dưới đây là các phương pháp điều trị bệnh {self.current_pick_disease.name}"
                    )
                    self.current_pick_disease.print_treatments()
                if "phòng bệnh" in u_in.lower().strip():
                    print(
                        f"Dưới đây là các phương pháp phòng chống bệnh {self.current_pick_disease.name}"
                    )
                    self.current_pick_disease.print_prevention()
                if "toàn bộ" in u_in.lower().strip():
                    print(
                        f"Dưới đây là toàn bộ thông tin liên quan tới bệnh {self.current_pick_disease.name}"
                    )
                    self.current_pick_disease.print_all()
                if "kết thúc" in u_in.lower().strip():
                    print(
                        f"Bạn đã chọn dừng tiếp nhận thông tin về bệnh {self.current_pick_disease.name}"
                    )
                    break
        print("Cảm ơn bạn đã sử dụng dịch vụ tra cứu thông tin bệnh thú y")

    def get_avail_diseases(self):
        if self.current_species == "cattle":
            return self.find_diseases_animal_based(self.current_animal, self.r_cattle)
        if self.current_species == "poultry":
            return self.find_diseases_animal_based(self.current_animal, self.r_poultry)
        return self.find_diseases_animal_based(
            self.current_similar_animals, self.r_cattle + self.r_poultry
        )

    # iterate through every diseases
    def find_diseases_animal_based(self, a_names=[""], diseases=[]):
        ret = []
        for disease in diseases:
            for name in a_names:
                if name.lower() in disease["species"]:
                    ret.append(disease)
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
        print(
            "Đầu tiên, bạn có thể cho tôi biết tên loại thuốc bạn đang tìm kiếm là gì không?"
        )
        pass
