from abc import ABC, abstractmethod
from models import Ninja, Mision

# Visitor abstracto
class ExportVisitor(ABC):
    @abstractmethod
    def visit_ninja(self, ninja: Ninja):
        pass

    @abstractmethod
    def visit_mision(self, mision: Mision):
        pass


# Concrete Visitor: Exportar a CSV
class CSVExportVisitor(ExportVisitor):
    def __init__(self):
        self.output = []

    def visit_ninja(self, ninja: Ninja):
        self.output.append(f"NINJA,{ninja.id},{ninja.nombre},{ninja.rango},{ninja.aldea.nombre}")

    def visit_mision(self, mision: Mision):
        self.output.append(f"MISION,{mision.id},{mision.nombre},{mision.rango},{mision.recompensa}")

    def get_result(self):
        return "\n".join(self.output)


# Concrete Visitor: Exportar a JSON
class JSONExportVisitor(ExportVisitor):
    def __init__(self):
        self.data = {"ninjas": [], "misiones": []}

    def visit_ninja(self, ninja: Ninja):
        self.data["ninjas"].append({
            "id": ninja.id,
            "nombre": ninja.nombre,
            "rango": ninja.rango,
            "aldea": ninja.aldea.nombre,
            "ataque": ninja.ataque,
            "defensa": ninja.defensa,
            "chakra": ninja.chakra
        })

    def visit_mision(self, mision: Mision):
        self.data["misiones"].append({
            "id": mision.id,
            "nombre": mision.nombre,
            "rango": mision.rango,
            "recompensa": mision.recompensa
        })

    def get_result(self):
        import json
        return json.dumps(self.data, indent=2)