import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ChartOptions, ChartType, ChartDataset, Chart } from 'chart.js';
import { Router } from '@angular/router';
import { SaisieBilanService } from '../../services/saisie-bilan.service';

// Import des éléments nécessaires de Chart.js
import {
  CategoryScale,
  LinearScale,
  BarElement,
  BarController,
  Legend,
  Title,
  Tooltip,
} from 'chart.js';

Chart.register(CategoryScale, LinearScale, BarElement, BarController, Legend, Title, Tooltip);

@Component({
  selector: 'app-saisie-bilan',
  templateUrl: './saisie-bilan.component.html',
  styleUrls: ['./saisie-bilan.component.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule],
})
export class SaisieBilanComponent implements OnInit {
  bilanId: any;
  prescription: any;
  mesures: { mesure: string; valeur: string }[] = [];
  newMesure = '';
  newValeur = '';
  showGraph = false;

  // Chart.js configuration
  chartData: ChartDataset[] = [];
  chartLabels: string[] = [];
  chartOptions: ChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };
  chartType: ChartType = 'bar';

  @ViewChild('chartCanvas', { static: false }) chartCanvas!: ElementRef<HTMLCanvasElement>;
  chart: Chart | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private saisieBilanService: SaisieBilanService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.bilanId = params['id'];
      console.log('Bilan ID:', this.bilanId);
      if (this.bilanId) {
        this.loadPrescription(this.bilanId);
      } else {
        console.error('Bilan ID is missing.');
      }
    });
  }

  loadPrescription(id: number): void {
    this.saisieBilanService.getPrescription(id).subscribe({
      next: (response) => {
        console.log('Prescription data:', response);
        this.prescription = response;
      },
      error: (error) => {
        console.error('Error loading prescription:', error);
      },
    });
  }

  addMesure(): void {
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

  sendToBackend(): void {
    if (this.mesures.length > 0) {
      const measures = JSON.stringify(this.mesures);
      this.saisieBilanService.postResults(this.bilanId, measures).subscribe({
        next: (response) => {
          console.log('Results posted successfully:', response);
        },
        error: (error) => {
          console.error('Error posting results:', error);
        },
      });
    } else {
      alert('Please add some measurements before submitting.');
    }
  }

  generateGraph(): void {
    const tab1 = this.mesures.map((m) => m.mesure);
    const tab2 = this.mesures.map((m) => +m.valeur);

    if (tab1.length === 0 || tab2.length === 0) {
      alert('Veuillez ajouter des mesures avant de générer le graphique.');
      return;
    }

    this.chartLabels = tab1;
    this.chartData = [
      {
        label: 'Mesures',
        data: tab2,
        backgroundColor: '#36A2EB',
        borderColor: '#1E88E5',
        borderWidth: 1,
      },
    ];

    this.showGraph = true;

    setTimeout(() => {
      if (this.chartCanvas && this.chartCanvas.nativeElement) {
        const ctx = this.chartCanvas.nativeElement.getContext('2d');
        if (ctx) {
          if (this.chart) {
            this.chart.destroy();
          }

          this.chart = new Chart(ctx, {
            type: this.chartType,
            data: {
              labels: this.chartLabels,
              datasets: this.chartData,
            },
            options: this.chartOptions,
          });
        } else {
          console.error('Failed to get canvas context.');
        }
      } else {
        console.error('Canvas element not found.');
      }
    }, 0);
  }
}