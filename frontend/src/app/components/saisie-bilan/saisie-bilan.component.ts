import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ChartOptions, ChartType, ChartDataset } from 'chart.js';


@Component({
  selector: 'app-saisie-bilan',
  templateUrl: './saisie-bilan.component.html',
  styleUrls: ['./saisie-bilan.component.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule],  // Added necessary modules
})
export class SaisieBilanComponent implements OnInit {
  bilanId: string | null = null;
  mesures: { mesure: string; valeur: string }[] = [];
  newMesure = '';
  newValeur = '';
  showGraph = false;

  // Chart.js configuration
  chartData: Record<string, ChartDataset[]> = {};
  chartLabels: Record<string, string[]> = {};
  chartOptions: ChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };
  chartType: ChartType = 'line';

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    // Retrieve 'id' from query params
    this.route.queryParams.subscribe((params) => {
      this.bilanId = params['id'];
      console.log('Bilan ID:', this.bilanId); // Check if the parameter is retrieved correctly
    });
  }

  // Helper function to extract keys from an object
  getKeys(obj: object): string[] {
    return Object.keys(obj);
  }

  // Add new measurement to the list
  addMesure() {
    if (this.newMesure.trim() && this.newValeur.trim()) {
      const newEntry = { mesure: this.newMesure, valeur: this.newValeur };
      this.mesures.push(newEntry);
      this.newMesure = '';
      this.newValeur = '';
      console.log('Measure added:', newEntry);
    } else {
      alert('Please fill in both fields before adding.');
    }
  }

  // Send the measurements to the backend (or log it)
  sendToBackend() {
    if (this.mesures.length > 0) {
      const dataToSend = { mesures: this.mesures };
      console.log('Data ready to send to backend:', JSON.stringify(dataToSend));
    } else {
      alert('No measures to send to the backend.');
    }
  }

  // Generate a graph based on the collected measurements
  /*
  genererGraphique() {
    if (this.mesures.length === 0) {
      alert('No data available to generate a graph.');
      return;
    }

    const transformedData: { [key: string]: { dates: string[]; values: number[] } } = {};

    // Transform the data into a format suitable for chart.js
    this.mesures.forEach((mesure) => {
      const { mesure: metric, valeur } = mesure;

      if (!transformedData[metric]) {
        transformedData[metric] = { dates: [], values: [] };
      }

      transformedData[metric].dates.push(new Date().toLocaleDateString());
      transformedData[metric].values.push(parseFloat(valeur));
    });

    // Update chart data and labels
    Object.keys(transformedData).forEach((metric) => {
      this.chartData[metric] = [
        {
          data: transformedData[metric].values,
          label: metric,
          fill: false,
          borderColor: 'blue',
          tension: 0.1,
        },
      ];
      this.chartLabels[metric] = transformedData[metric].dates;
    });

    // Show the graph after it's generated
    this.showGraph = true;
  }
  */
}

