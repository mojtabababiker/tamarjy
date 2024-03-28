#!/usr/bin/env python3
""" Tamarjy Console Application for testing and 
    running the application on the console
"""
from cmd import Cmd
import json
from models import storage, predictor
from models.user import User
from models.disease import Disease
from models.clinic import Clinic


class TamarjyConsole(Cmd):
    """The Tamarjy console application"""
    prompt = "Tamarjy> "
    intro = "Welcome to Tamarjy console application"

    def __init__(self):
        super().__init__()
        self.predictor = predictor
        self.storage = storage

    def emptyline(self) -> bool:
        return False

    def do_EOF(self, arg):
        """Exit the application"""
        print("Have a good one!")
        return True

    def do_exit(self, arg):
        """Exit the application"""
        print("Have a good one!")
        return True

    def do_predict(self, arg):
        """Predict the disease from the given symptoms"""
        result = self.predictor.predict(arg)
        if not result:
            print("No disease found for the given symptoms!")
            for s in self.predictor.extracted_symptoms:
                print(f"\t* Symptom: {s}")
            return False
        print(f"The predicted diseases for the [{self.predictor.extracted_symptoms}] are:")
        for disease, probability in result.items():
            print(f"{disease}: {probability}")

    def do_create(self, arg):
        """Create a user or a disease"""
        args = arg.split()
        if len(args) < 2:
            print("Usage: create <user/disease> <kwargs>")
            return False
        if args[0] == "user":
            if len(args) < 9:
                print("Usage: create user first_name='<first_name>' " +
                      "last_name='<last_name>' email='<email>' " +
                      "password=<password> phone=<phone> " +
                      "gender=<gender> age=<age> address='<address>'")
                return False
            try:
                kwargs = {k: v for k, v in [a.split('=') for a in args[1:]]}
                user = User(**kwargs)
                user.save()
                print(f"User {user.id} created successfully")
            except Exception as e:
                raise e
                print("Invalid arguments")
                return False

        elif args[0] == "disease":
            if len(args) < 4:
                print("Usage: create disease name='<name>' " +
                      "description='<description>' specialty='<specialty>'")
                return False
            try:
                kwargs = {k: v for k, v in [a.split('=') for a in args[1:]]}
                disease = Disease(**kwargs)
                disease.save()
                print(f"Disease {disease.id} created successfully")
            except Exception as e:
                raise e
                print("Invalid arguments")
                return False
        elif args[0] == "clinic":
            if len(args) < 9:
                print("Usage: create clinic name='<name>' " +
                      "latitude=<latitude> longitude=<longitude> " +
                      "phone='<phone>' email='<email>' doctor='<doctor>' " +
                      "specialty='<specialty>' website='<website>' "
                      )
                return False
            try:
                kwargs = {k: v.replace("'", '').replace('_', ' ') for k, v in [a.split('=') for a in args[1:]]}
                clinic = Clinic(**kwargs)
                clinic.save()
                print(f"Clinic {clinic.id} created successfully")
            except Exception as e:
                print(e)
                print("Invalid arguments")
                return False
        storage.close()  # force committing and closing the session

    def do_disease(self, arg):
        """create all the diseases  will be deleted later"""
        with open('/home/mojtaba/Downloads/diseases_sql.json', 'r', encoding='utf-8') as f:
            diseases_dict = json.load(f)
        diseases = diseases_dict['Name']
        desc = diseases_dict['description']
        prec = diseases_dict['precautions']
        spec = diseases_dict['specialty']
        for i in range(len(diseases)):
            disease_ = Disease(
                name=diseases[f"{i}"],
                description=desc[f"{i}"],
                precautions=prec[f"{i}"],
                specialty=spec[f"{i}"]
            )
            disease_.save()
            print(f"Disease {disease_.id} created successfully")

    def do_get(self, arg):
        """get the users or diseases based on the id if provided"""
        args = arg.split()
        if not args:
            print("Usage: get <user/disease> [id]")

        elif len(args) == 1:
            objs = storage.get(args[0])
            for obj in objs:
                print(obj)
        else:
            objs = storage.get(args[0], {'id': args[1]})
            for obj in objs:
                print(obj)

if __name__ == "__main__":
    TamarjyConsole().cmdloop()
