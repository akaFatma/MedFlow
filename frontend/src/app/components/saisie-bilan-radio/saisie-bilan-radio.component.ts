import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ChartOptions, ChartType, ChartDataset } from 'chart.js';
import { Router } from '@angular/router';  // Import Router
import { SaisieBilanService } from '../../services/saisie-bilan.service';

@Component({
  selector: 'app-saisie-bilan-radio',
  templateUrl: './saisie-bilan-radio.component.html',
  styleUrls: ['./saisie-bilan-radio.component.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule],  // Added necessary modules
})
export class SaisieBilanRadioComponent implements OnInit {
  bilanId: any;
  prescription: any;
  compteRendu = '';
  image: any;
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

  constructor(private route: ActivatedRoute, private router: Router, 
              private saisieBilanService: SaisieBilanService
  ) {}  // Inject Router here

  ngOnInit(): void {
    // Retrieve 'id' from query params
    this.route.queryParams.subscribe((params) => {
      this.bilanId = params['id'];
      console.log('Bilan ID:', this.bilanId); // Check if the parameter is retrieved correctly
    });
      this.loadPrescription(this.bilanId);
    }

    loadPrescription(id: number): void {
      this.saisieBilanService.getPrescriptionRadio(id).subscribe({
        next: (response) => {
          console.log('Prescription data:', response);
          this.prescription = response;
        },
        error: (error) => {
          console.error('Error loading prescription:', error);
        }
      });
    }


  // Helper function to extract keys from an object
  getKeys(obj: object): string[] {
    return Object.keys(obj);
  }


  // Send the measurements to the backend (or log it)
  sendToBackend() {
    console.log(this.compteRendu);
      this.saisieBilanService.postCompteRendu(this.bilanId, this.compteRendu).subscribe({
      next: (response) => {
        console.log('Compte rendu posted successfully:', response);
      },
      error: (error) => {
        console.error('Error posting results:', error);
      }
      });
    }
}

