import os
import matplotlib.pyplot as plt
import numpy as np
from database import DataBase

class GraphGenerator:
    
    def __init__(self, db: DataBase, top_perf: int = 500):
        self.db = db
        self.top_perf = top_perf
        self.rows = []  # Initialisation par sécurité
        self._fetch_query()
        
    def _fetch_query(self):
        # On retire le filtre 'WHERE n.name LIKE "%1M%"' pour tout avoir en mémoire
        query = f"""
            SELECT n.name, t.time
            FROM {self.db.time_table} t
            JOIN {self.db.push_type_table} n ON t.push_id = n.push_id
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
        # On filtre ici pour ne garder que le 1M pour les deux premiers graphs
        data_by_method_1m = {
            name: times[-10:] 
            for name, times in self._get_all_data_by_method().items() 
            if "1M" in name
        }
        
        self._create_chart(
            data_by_method_1m,
            "Évolution du Temps Cumulé - Toutes les méthodes (Max 10 itérations)",
            "plots/benchmark_all_methods.png"
        )

        top_performers = self._get_top_performers(data_by_method_1m)
        self._create_chart(
            top_performers,
            f"L'Élite - Uniquement les méthodes rapides (< {self.top_perf}s au cumul)",
            "plots/benchmark_top_performers.png"
        )
        
    def _get_all_data_by_method(self):
        """Regroupe l'intégralité des données brutes de self.rows par méthode"""
        data_by_method = {}
        for method_name, exec_time in self.rows:
            if method_name not in data_by_method:
                data_by_method[method_name] = []
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
            "#ff4500", "#00d2ff", "#39ff14", "#ff007f", "#ffcc00", "#00ffcc",
            "#9933ff", "#ff6600", "#ff3333", "#bfff00", "#0080ff", "#ff00ff",
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
        

    def generate_comparison_plot(self):
        volumes = [1000, 100000, 1000000]
        
        methods_data = {
            "Executemany": ["Executemany 1k", "Executemany 100k", "Executemany 1M"],
            "Execute Batches": ["Execute_batch 1k (page_size=100)", "Execute_batch 100k (page_size=1000)", "Execute_batch 1M (page_size=10000)"],
            "COPY Expert": ["COPY Expert 1k", "COPY Expert 100k", "COPY Expert 1M"],
            "Pandas Default": ["Pandas Default 1k", "Pandas Default 100k", "Pandas Default 1M"],
            "Pandas Multi": ["Pandas Multi 1k", "Pandas Multi 100k", "Pandas Multi 1M"],
            "Pandas Callable COPY": ["Pandas Callable COPY 1k", "Pandas Callable COPY 100k", "Pandas Callable COPY 1M"],
            "COPY Stream Tuple": ["COPY Stream Tuple 1k", "COPY Stream Tuple 100k", "COPY Stream Tuple 1M"]
        }

        all_data = self._get_all_data_by_method()

        plt.figure(figsize=(13, 8))

        for method_name, db_labels in methods_data.items():
            medians = []
            for label in db_labels:
                times = all_data.get(label)
                if times:
                    medians.append(np.median(times))
                else:
                    medians.append(None)
            
            if None not in medians:
                # Ajout de markers plus visibles et d'une ligne légèrement plus épaisse
                plt.plot(volumes, medians, marker='o', markersize=6, linewidth=2.5, label=method_name)

        # --- AMÉLIORATION DE LA LISIBILITÉ ---
        plt.xscale('log')
        plt.yscale('log') # Échelle log sur Y pour étirer les petits temps d'exécution
        
        plt.xlabel("Volume de données (nombre de lignes, échelle log)", fontsize=11, labelpad=10)
        plt.ylabel("Temps d'exécution médian (secondes, échelle log)", fontsize=11, labelpad=10)
        plt.title("Comparatif des performances d'insertion : Zoom sur les croisements", fontsize=14, fontweight='bold', pad=15)
        
        # Forcer les repères sur l'axe X
        plt.xticks(volumes, ['1k', '100k', '1M'])
        
        # Formater l'axe Y pour avoir des secondes claires au lieu de notations scientifiques compliquées
        import matplotlib.ticker as ticker
        ax = plt.gca()
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))
        
        # Grille plus précise pour suivre les lignes de croisement
        plt.grid(True, which="both", linestyle="--", alpha=0.6)
        
        # Positionnement de la légende à l'extérieur ou dans un coin dégagé
        plt.legend(loc="upper left", frameon=True, shadow=True, facecolor="white")
        plt.tight_layout()

        os.makedirs("plots", exist_ok=True)
        plt.savefig("plots/benchmark_evolution_curves.png", dpi=300)
        plt.close()
        print("Graphique d'évolution optimisé généré dans 'plots/benchmark_evolution_curves.png'")
        
        
    def generate_focused_comparison_plot(self):
        # 1. On définit les volumes de données (Axe X)
        volumes = [1000, 100000, 1000000]
        
        # 2. Configuration des méthodes cibles et de leurs libellés en base
        methods_data = {
            "Pandas Callable COPY": [
                "Pandas Callable COPY 1k", 
                "Pandas Callable COPY 100k", 
                "Pandas Callable COPY 1M"
            ],
            "COPY Stream Tuple": [
                "COPY Stream Tuple 1k", 
                "COPY Stream Tuple 100k", 
                "COPY Stream Tuple 1M"
            ]
        }

        # Récupération de l'ensemble du dictionnaire global en mémoire
        all_data = self._get_all_data_by_method()

        plt.figure(figsize=(11, 6))

        # 3. Calcul des médianes et tracé
        for method_name, db_labels in methods_data.items():
            medians = []
            for label in db_labels:
                times = all_data.get(label)
                if times:
                    medians.append(np.median(times))
                else:
                    medians.append(None)
            
            # Tracé si au moins une partie des données existe
            if any(m is not None for m in medians):
                plt.plot(volumes, medians, marker='o', markersize=8, linewidth=2.5, label=method_name)

        # 4. Configuration des axes (Double Échelle Logarithmique)
        plt.xscale('log')
        plt.yscale('log')
        
        plt.xlabel("Volume de données (nombre de lignes, échelle log)", fontsize=11, labelpad=10)
        plt.ylabel("Temps d'exécution médian (secondes, échelle log)", fontsize=11, labelpad=10)
        
        # Titre mis à jour
        plt.title("Zoom : Pandas Callable COPY vs COPY Stream Tuple", fontsize=13, fontweight='bold', pad=15)
        
        # Forcer les graduations textuelles sur X
        plt.xticks(volumes, ['1k', '100k', '1M'])
        
        # Rendre l'axe Y plus lisible (chiffres classiques plutôt que notation scientifique)
        import matplotlib.ticker as ticker
        ax = plt.gca()
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))
        
        # Grille complète pour repérer les intersections
        plt.grid(True, which="both", linestyle="--", alpha=0.6)
        plt.legend(loc="upper left", frameon=True, shadow=True)
        plt.tight_layout()

        # 5. Sauvegarde dédiée
        os.makedirs("plots", exist_ok=True)
        output_path = "plots/copy_methods_comparison.png"
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"Graphique ciblé généré avec succès dans : {os.path.abspath(output_path)}")