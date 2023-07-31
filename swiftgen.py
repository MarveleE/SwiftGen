import os
import sys
import argparse
import time


def current_path():
    return os.getcwd()


def static_file_path():
    if getattr(sys, 'frozen', None):
        return sys._MEIPASS
    else:
        return os.path.dirname(__file__)


class TemplateCenter:
    template_path = static_file_path()

    @classmethod
    def create_viewcontroller(self):
        content = self.get_template(by="vc")
        content = self.replace_keyword(content, text=feature, key="Template")
        return content

    @classmethod
    def create_swiftui(self):
        content = self.get_template(by="swiftui")
        content = self.replace_keyword(content, text=feature, key="Template")
        return content

    @classmethod
    def create_usecase(self):
        content = self.get_template(by="usecase")
        content = self.replace_keyword(content, text=feature, key="Template")
        return content

    @classmethod
    def create_repository(self):
        content = self.get_template(by="repository")
        content = self.replace_keyword(content, text=feature, key="Template")
        return content

    @classmethod
    def create_viewmodel(self):
        content = self.get_template(by="viewmodel")
        content = self.replace_keyword(content, text=feature, key="Template")
        return content

    @classmethod
    def get_template(self, by: str):
        author_path = self.template_path + f"/author.txt"
        author_content = ""
        with open(author_path, "r") as f:
            content = f.read()
            content = self.replace_keyword(
                content, text=author, key="AUTHOR")
            content = self.replace_keyword(
                content, text=self.get_date(), key="DATE")
            content = self.replace_keyword(
                content, text=file_name, key="FILENAME")
            author_content = content
        if by != "":
            with open(self.template_path + f"/{by}.txt", "r") as f:
                content = f.read()
                return str(author_content) + str(content)
        return author_content

    def replace_keyword(content: str, text: str, key: str) -> str:
        # find "Template" and replace it with key
        return content.replace(key, text)

    @classmethod
    def get_date(self):
        return time.strftime("%Y-%m-%d", time.localtime())


def create_folders(feature: str):
    # create folders and files in current path
    for folder in paths(feature):
        root = current_path()+folder
        path = "/".join(root.split("/")[0:-1])
        global file_name
        file_name = root.split("/")[-1]

        if not os.path.exists(path):
            os.makedirs(path)
        with open(root, "w+") as f:
            if root.endswith("ViewController.swift"):
                f.write(TemplateCenter.create_viewcontroller())
            elif root.endswith("ViewModel.swift"):
                f.write(TemplateCenter.create_viewmodel())
            elif root.endswith(f"{feature}.swift"):
                f.write(TemplateCenter.get_template(by=""))
            elif root.endswith("Repository.swift"):
                f.write(TemplateCenter.create_repository())
            elif root.endswith("UseCase.swift"):
                f.write(TemplateCenter.create_usecase())
        print(f"Create folder: {root}")

    print("✅ Done!")


def paths(feature: str):
    return [
        f"/{feature}/Presentaion/View/{feature}ViewController.swift",
        f"/{feature}/Presentaion/ViewModel/{feature}ViewModel.swift",
        f"/{feature}/Data/Entities/{feature}.swift",
        f"/{feature}/Data/API/{feature}.swift",
        f"/{feature}/Data/Repository/{feature}Repository.swift",
        f"/{feature}/Domain/{feature}UseCase.swift",
    ]


if __name__ == "__main__":
    feature = ""
    file_name = ""
    author = ""
    parser = argparse.ArgumentParser(description="Your script description")
    parser.add_argument("-author", help="Your name")
    parser.add_argument("-feature", help="Your name")
    args = parser.parse_args()
    if args.author:
        author = args.author
    if args.feature:
        feature = args.feature
        print(f"Feature: {args.feature}")
        create_folders(feature)
