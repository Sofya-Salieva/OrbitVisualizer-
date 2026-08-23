
using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Windows;
using System.Windows.Media.Media3D;

namespace Orbit_Visualizer;

public partial class MainWindow : Window
{
    private static readonly HttpClient httpClient = new()
    {
        BaseAddress = new Uri("http://localhost:8000")
    };

    public MainWindow()
    {
        InitializeComponent();
    }

    private async void CalculateButton_Click(object sender, RoutedEventArgs e)
    {
        StatusBlock.Text = "Рассчитываю...";
        try
        {
            var request = new
            {
                altitude_km = double.Parse(AltitudeBox.Text),
                inclination_deg = double.Parse(InclinationBox.Text),
                eccentricity = 0.0,
                raan_deg = 0.0,
                arg_perigee_deg = 0.0,
                dt = 60.0,
                num_points = 100
            };

            var json = JsonSerializer.Serialize(request);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            // Отправляем POST на /orbit
            var response = await httpClient.PostAsync("/orbit", content);
            response.EnsureSuccessStatusCode();

            var responseBody = await response.Content.ReadAsStringAsync();
            var orbitResponse = JsonSerializer.Deserialize<OrbitResponse>(responseBody);

            // Преобразуем в точки и обновляем линию
            var points = new Point3DCollection();
            foreach (var point in orbitResponse.Trajectory)
            {
                double scale = 1.0 / 1000000;
                points.Add(new Point3D(point[0] * scale, point[1] * scale, point[2] * scale));
            }
            OrbitLine.Points = points;
            StatusBlock.Text = $"Орбита построена ({points.Count} точек)";
        }
        catch (Exception ex)
        {
            StatusBlock.Text = $"Ошибка: {ex.Message}";
        }
    }
        
}

public class OrbitResponse
{

    [JsonPropertyName("trajectory")] 
    public List<List<double>> Trajectory { get; set; }
}