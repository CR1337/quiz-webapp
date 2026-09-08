import zipfile
import io
import os
from typing import Set


class QuestionExporter:
    DATA_DIRECTORY: str = "data"
    IMAGES_DIRECTORY: str = "images"
    QUESTION_IMAGES_DIRECTORY: str = f"{IMAGES_DIRECTORY}/questions"

    QUESTIONS: str = f"{DATA_DIRECTORY}/questions.json"
    CONFIG: str = f"{DATA_DIRECTORY}/config.json"
    DYNAMIC_LOCALIZTION: str = f"{DATA_DIRECTORY}/dynamic_localization.json"

    INTRO_IMAGE_DE: str = f"{IMAGES_DIRECTORY}/title0_de.png"
    INTRO_IMAGE_EN: str = f"{IMAGES_DIRECTORY}/title0_en.png"

    OUTRO_IMAGE_DE: str = f"{IMAGES_DIRECTORY}/result_de.png"
    OUTRO_IMAGE_EN: str = f"{IMAGES_DIRECTORY}/result_en.png"

    INTRO_OUTRO_IMAGES: Set[str] = set([
        INTRO_IMAGE_DE, INTRO_IMAGE_EN, OUTRO_IMAGE_DE, OUTRO_IMAGE_EN
    ])

    OUTPUT_FILENAME: str = "quiz.zip"

    @classmethod
    def export(cls):
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            cls.copy_file(zf, cls.QUESTIONS)
            cls.copy_file(zf, cls.CONFIG)
            cls.copy_file(zf, cls.DYNAMIC_LOCALIZTION)

            cls.copy_file(zf, cls.INTRO_IMAGE_DE)
            cls.copy_file(zf, cls.INTRO_IMAGE_EN)
            cls.copy_file(zf, cls.OUTRO_IMAGE_DE)
            cls.copy_file(zf, cls.OUTRO_IMAGE_EN)

            image_filenames = [
                f"{cls.QUESTION_IMAGES_DIRECTORY}/{filename}"
                for filename in os.listdir(cls.QUESTION_IMAGES_DIRECTORY)
            ]

            for filename in image_filenames:
                cls.copy_file(zf, filename)

        zip_buffer.seek(0)

        with open(cls.OUTPUT_FILENAME, "wb") as file:
            file.write(zip_buffer.read())

    @classmethod
    def copy_file(cls, zf: zipfile.ZipFile, filename: str):
        with open(filename, "rb") as file:
            data = file.read()

        zf.writestr(filename, data)


if __name__ == "__main__":
    exporter = QuestionExporter()
    exporter.export()