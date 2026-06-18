import os
import matplotlib.pyplot as plt
import numpy as np
from database import DataBase

class GraphGenerator:
    
    def __init__(self, db: DataBase, top_perf: int = 500):
        self.db = db
        self.top_perf = top_perf
        self._fetch_query()
        
    def _fetch_query(self):
        query = f"""
            SELECT n.name, t.time
            FROM {self.db.time_table} t
            JOIN {self.db.push_type_table} n ON t.push_id = n.push_id
            WHERE n.name LIKE '%1M%'
            ORDER BY n.name, t.time_id;
        """

        try:
            self.db.cursor.execute(query)
            self.rows = self.db.cursor.fetchall()
            if not self.rows:
                print("No data in tables")
                return
        except Exception as e:
            print(f"Err from db: {e}")
            return
        finally:
            self.db.cursor.close()
            self.db.conn.close()

    def generate_filtered_plots(self):
        
        data_by_method = self._get_data_by_method()

        self._create_chart(
            data_by_method,
            "Évolution du Temps Cumulé - Toutes les méthodes (Max 10 itérations)",
            "benchmark_all_methods.png"
        )

        top_performers = self._get_top_performers(data_by_method)

        self._create_chart(
            top_performers,
            f"L'Élite - Uniquement les méthodes rapides (< {self.top_perf}s au cumul)",
            "benchmark_top_performers.png"
        )
        
    def _get_data_by_method(self):
        data_by_method = {}
        for method_name, exec_time in self.rows:
            if method_name not in data_by_method:
                data_by_method[method_name] = []

            if len(data_by_method[method_name]) < 10:
                data_by_method[method_name].append(float(exec_time))
        return data_by_method
    
    def _get_top_performers(self, data_by_method):
        top_performers = {}
        for method_name, times in data_by_method.items():
            if sum(times) < self.top_perf:
                top_performers[method_name] = times
        return top_performers
        
    def _create_chart(self, dataset, title, filename):
        if not dataset:
            print(f"No dataset for : {title}")
            return
        
        markers = ["o", "s", "^", "D", "x", "v", "<", ">", "p", "*", "h", "+"]
        colors = [
            "#ff4500",
            "#00d2ff",
            "#39ff14",
            "#ff007f",
            "#ffcc00",
            "#00ffcc",
            "#9933ff",
            "#ff6600",
            "#ff3333",
            "#bfff00",
            "#0080ff",
            "#ff00ff",
        ]

        plt.figure(figsize=(14, 8), facecolor="#1e1e1e")
        ax = plt.gca()
        ax.set_facecolor("#252525")

        for idx, (method_name, times) in enumerate(dataset.items()):
            cumulated_times = np.cumsum(times)
            iterations = range(1, len(times) + 1)

            plt.plot(
                iterations,
                cumulated_times,
                label=method_name,
                linewidth=2.5,
                marker=markers[idx % len(markers)],
                markersize=6,
                color=colors[idx % len(colors)],
            )

        plt.title(title, color="white", fontsize=14, fontweight="bold", pad=20)
        plt.xlabel("Itérations", color="white", fontsize=11, labelpad=10)
        plt.ylabel(
            "Temps total cumulé (Secondes) - Plus bas = Meilleur",
            color="white",
            fontsize=11,
            labelpad=10,
        )

        plt.grid(True, linestyle="--", alpha=0.15, color="white")
        plt.xticks(range(1, 11))
        ax.tick_params(colors="white")

        legend = plt.legend(
            facecolor="#1e1e1e",
            edgecolor="gray",
            loc="upper left",
            bbox_to_anchor=(1.02, 1),
        )
        for text in legend.get_texts():
            text.set_color("white")

        plt.tight_layout()
        plt.savefig(filename, dpi=300, facecolor=plt.gcf().get_facecolor())
        plt.close()
        print(f"Graphique généré : {os.path.abspath(filename)}")