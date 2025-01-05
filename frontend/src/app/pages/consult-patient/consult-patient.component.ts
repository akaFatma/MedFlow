import { Component, OnInit } from '@angular/core';
import { ConsultationPatientService } from '../../services/consult-patient.service';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-consult-patient',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './consult-patient.component.html',
  styleUrl: './consult-patient.component.scss',
})
export class ConsultPatientComponent implements OnInit {
  errorMessage: string = '';
  CONSULTATION: any;

  showRadio: boolean = false;
  loading: boolean = false;

  constructor(
    private consultPatientService: ConsultationPatientService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  goToHomePage() {
    this.router.navigate(['/HomePage']);
  }
  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      const id = params['id'];
      console.log('Query Param ID:', id);
      if (id) {
        this.loadConsultationInfo(Number(id));
      }
    });
  }

  loadConsultationInfo(id: number): void {
    this.loading = true;
    this.consultPatientService.getConsultation(id).subscribe({
      next: (data) => {
        console.log('Received Data:', data);
        this.CONSULTATION = data;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching consultation info:', error);
        this.loading = false;
      },
    });
  }

  onConsult(id: number): void {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { id: id },
      queryParamsHandling: 'merge',
    });
    this.loadConsultationInfo(id);
  }

  reloadConsultation(): void {
    if (this.CONSULTATION) {
      console.log('Reloading Consultation:', this.CONSULTATION);
      this.loadConsultationInfo(this.CONSULTATION.id);
    } else {
      console.warn('No Consultation available to reload.');
    }
  }

  logConsultationData(): void {
    if (this.CONSULTATION) {
      console.log('Consultation Data:', this.CONSULTATION);
    } else {
      console.warn('No Consultation Data to Log.');
    }
  }

  onViewRadio(): void {
    this.showRadio = !this.showRadio;
  }

  getImageRadio(index: number): void {
    if (!this.CONSULTATION?.data?.bilans_radiologiques_url_image?.[index]) {
      console.error('No image URL found for index:', index);
      return;
    }
    const imageURL = this.CONSULTATION.data.bilans_radiologiques_url_image[index];
    
    this.loading = true;
    this.consultPatientService.getImageRadio(imageURL).subscribe({
      next: (response: Blob) => {
        // Create a blob URL and trigger download
        const url = window.URL.createObjectURL(response);
        const link = document.createElement('a');
        link.href = url;
        link.download = `radiographie_${index + 1}.jpg`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        this.loading = false;
      },
      error: (error) => {
        console.error('Error downloading radiography:', error);
        this.errorMessage = 'Erreur lors du téléchargement de la radiographie';
        this.loading = false;
      }
    });
  }
  
}
