import { Component, OnInit } from '@angular/core';
import { ConsultationPatientService} from '../../services/consult-patient.service';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-consult-patient',
  imports: [CommonModule],
  templateUrl: './consult-patient.component.html',
  styleUrl: './consult-patient.component.scss'
})
export class ConsultPatientComponent implements OnInit {
  errorMessage = '';
  CONSULTATION: any;
  constructor(
    private consultPatientService: ConsultationPatientService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const id = params['id'];
      console.log(id);
      if (id) {
        this.loadConsultationInfo(id);
      }
    });
  }

  loadConsultationInfo(id : number): void {
    this.consultPatientService.getConsultation(id).subscribe({
      next: (data) => {
        console.log('Data:', data);
        this.CONSULTATION = data;
        console.log('Consultation:', this.CONSULTATION);
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching Consultation info:', error);
      }
    });
  }
}

