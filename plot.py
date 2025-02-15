import matplotlib.pyplot as plt

# Beispiel-Daten
angles = [-135, -90, -45, 0, 45, 90, 135]
distances = [100, 250, 20, 5, 15, 10, 100]

# Erstelle den Plot
plt.figure(figsize=(10, 6))
plt.bar([str(angle) for angle in angles], distances, color="skyblue")

# Titel und Achsenbeschriftungen mit verbesserter Typografie
plt.title("Car Radar Sensor Data - Generation 0", fontsize=18, fontweight='bold', pad=20)
plt.xlabel("Radar Angle (degrees)", fontsize=20, labelpad=10)
plt.ylabel("Distance Detected", fontsize=20, labelpad=10)

# Achsenbeschriftungen anpassen
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

# Gitterlinien hinzufügen
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Speichere den Plot als Bild
plt.savefig("enhanced_radar_plot.png", dpi=300, bbox_inches='tight')

# Plot anzeigen
plt.show()
