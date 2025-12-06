import csv
from django.core.management.base import BaseCommand
from quiz.models import Molecula, Pergunta

class Command(BaseCommand):
    help = "Importa moléculas e perguntas dos CSV/TXT"

    def add_arguments(self, parser):
        parser.add_argument("--moleculas", type=str, help="CSV de moléculas")
        parser.add_argument("--perguntas_geral", type=str, help="CSV de perguntas gerais")
        parser.add_argument("--perguntas_moleculas", type=str, help="TXT de perguntas por molécula")

    def handle(self, *args, **options):

        # =====================================
        #  IMPORTAR MOLÉCULAS
        # =====================================
        if options["moleculas"]:
            path = options["moleculas"]
            self.stdout.write(self.style.SUCCESS(f"Importando moléculas de {path}"))

            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")

                for row in reader:

                    # Função para normalizar números como "16,04 g/mol"
                    def limpar_numero(valor):
                        if not valor:
                            return 0
                        valor = valor.replace("g/mol", "").replace("kg/m³", "")
                        valor = valor.replace("°C","").strip()
                        valor = valor.replace(",", ".")
                        try:
                            return float(valor)
                        except:
                            return 0

                    m, created = Molecula.objects.update_or_create(
                        nome=row["Nome"],
                        defaults={
                            "formula": row.get("Fórmula", ""),
                            "massaMolar": limpar_numero(row.get("Massa Molecular", "")),
                            "polaridade": row.get("Polaridade", ""),
                            "densidade": limpar_numero(row.get("Densidade", "")),
                            "pontoEbulicao": limpar_numero(row.get("Ponto Ebulição", "")),
                            "pontoFusao": limpar_numero(row.get("Ponto Fusão", "")),
                            "caracteristicas": row.get("Características", ""),
                            "geometria": row.get("Geometria", ""),
                            "fontes": row.get("Fontes", ""),
                            "aplicacoes": row.get("Aplicações", "")
                        }
                    )

            self.stdout.write(self.style.SUCCESS("✔ Moleculas importadas"))



        # =====================================
        #  IMPORTAR PERGUNTAS GERAIS
        # =====================================
        if options["perguntas_geral"]:
            path = options["perguntas_geral"]
            self.stdout.write(self.style.SUCCESS(f"Importando perguntas gerais de {path}"))

            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")

                for row in reader:
                    Pergunta.objects.create(
                        molecula=None,
                        enunciado=row["Enunciado"],
                        alternativa_a=row["Alternativa A"],
                        alternativa_b=row["Alternativa B"],
                        alternativa_c=row["Alternativa C"],
                        alternativa_d=row["Alternativa D"],
                        resposta_correta=row["Resposta Correta"].strip().lower(),
                        dificuldade=row.get("Dificuldade", "M"),
                        dica=row.get("Dica", ""),
                        referencia=row.get("Referência", "")
                    )


            self.stdout.write(self.style.SUCCESS("✔ Perguntas gerais importadas"))

        #  IMPORTAR PERGUNTAS POR MOLÉCULA (CSV ou TXT)
        # =====================================
        if options["perguntas_moleculas"]:
            path = options["perguntas_moleculas"]
            self.stdout.write(self.style.SUCCESS(f"Importando perguntas de moléculas de {path}"))

            # Detecta se é CSV (tem ; no header)
            with open(path, encoding="utf-8") as f:
                first_line = f.readline()

            if ";" in first_line and "Molécula" in first_line:
                self.stdout.write(self.style.SUCCESS("→ Detectado formato CSV"))

                with open(path, encoding="utf-8") as f:
                    reader = csv.DictReader(f, delimiter=";")

                    for row in reader:

                        nome = row["Molécula"].strip()

                        molecula = (
                            Molecula.objects.filter(nome__iexact=nome).first()
                            or Molecula.objects.filter(formula__iexact=nome).first()
                        )

                        if not molecula:
                            self.stdout.write(self.style.WARNING(f"Molecula NÃO encontrada: {nome}"))
                            continue

                        Pergunta.objects.create(
                            molecula=molecula,
                            enunciado=row["Enunciado"],
                            alternativa_a=row["Alternativa A"],
                            alternativa_b=row["Alternativa B"],
                            alternativa_c=row["Alternativa C"],
                            alternativa_d=row["Alternativa D"],
                            resposta_correta=row["Resposta Correta"].strip().lower(),
                            dificuldade=row.get("Dificuldade", "M"),
                            dica=row.get("Dica", ""),
                            referencia=row.get("Referência", "CSV Importado")
                        )

                self.stdout.write(self.style.SUCCESS("✔ Perguntas de moléculas (CSV) importadas"))
                return


    # Função auxiliar para salvar perguntas txt
    def _salvar_pergunta_molecula(self, molecula, buffer):
        """
        Formato esperado:
        ENUNCIADO: ...
        A: ..
        B: ..
        C: ..
        D: ..
        CORRETA: B
        DICA: ...
        DIFICULDADE: F/M/D
        REFERENCIA: ...
        """
        data = {}

        for line in buffer:
            if line.startswith("ENUNCIADO:"):
                data["enunciado"] = line.replace("ENUNCIADO:", "").strip()
            elif line.startswith("A:"):
                data["a"] = line[2:].strip()
            elif line.startswith("B:"):
                data["b"] = line[2:].strip()
            elif line.startswith("C:"):
                data["c"] = line[2:].strip()
            elif line.startswith("D:"):
                data["d"] = line[2:].strip()
            elif line.startswith("CORRETA:"):
                data["correta"] = line.replace("CORRETA:", "").strip().lower()
            elif line.startswith("DICA:"):
                data["dica"] = line.replace("DICA:", "").strip()
            elif line.startswith("DIFICULDADE:"):
                data["dificuldade"] = line.replace("DIFICULDADE:", "").strip()
            elif line.startswith("REFERENCIA:"):
                data["referencia"] = line.replace("REFERENCIA:", "").strip()

        Pergunta.objects.create(
            molecula=molecula,
            enunciado=data.get("enunciado", ""),
            alternativa_a=data.get("a", ""),
            alternativa_b=data.get("b", ""),
            alternativa_c=data.get("c", ""),
            alternativa_d=data.get("d", ""),
            resposta_correta=data.get("correta", "a"),
            dificuldade=data.get("dificuldade", "M"),
            dica=data.get("dica", ""),
            referencia=data.get("referencia", "TXT Importado")
        )
