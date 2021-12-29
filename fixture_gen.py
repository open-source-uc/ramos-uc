import os
import dotenv
import itertools
import django


def main():
    dotenv.read_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ramosuc.settings")
    django.setup()

    try:
        from django.core import serializers
        from django.contrib.admin.utils import NestedObjects
        from apps.courses.models import Course

        # nombre de la bdd
        collector = NestedObjects(using="default")
        # recolectar consulta de pocas instancias de un modelo
        collector.collect(Course.objects.all()[:20])

        # se obtienene los elementos relacionados
        objects = list(itertools.chain.from_iterable(collector.data.values()))

        with open("fixture.json", "w") as file:
            file.write(serializers.serialize("json", objects))

    except Exception as e:
        print("Cannot create fixture:", e)


if __name__ == "__main__":
    main()
