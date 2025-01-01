import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { BilanComponent } from '../../components/bilan/bilan.component';
import { OrdonnanceComponent } from '../../components/ordonnance/ordonnance.component';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
import { ResumeComponent } from '../../components/resume/resume.component';
import { ConsultationService } from '../../services/consultation.service';

@Component({
  selector: 'app-nouvelle-consultation',
  standalone: true,
  imports: [ReactiveFormsModule, BilanComponent, OrdonnanceComponent, BienvenuComponentComponent, ResumeComponent],
  templateUrl: './nouvelle-consultation.component.html',
  styleUrls: ['./nouvelle-consultation.component.scss']
})
export class NouvelleConsultationComponent implements OnInit {
  consultationForm!: FormGroup;
  bilanData: any = null;
  ordonnanceData: any = null;
  resumeData: string = '';
  nss: string = '123456789012345';  // NSS récupéré

  constructor(private fb: FormBuilder, private consultationservice: ConsultationService) {}

  ngOnInit(): void {
    this.consultationForm = this.fb.group({
      bilan: [null, Validators.required],
      ordonnance: [null, Validators.required],
      resume: ['', Validators.required]
    });
  }

  // Lors de la soumission du bilan
  onBilanSubmit(data: any) {
    this.bilanData = data;
  }

  // Lors de la soumission de l'ordonnance
  onOrdonnanceSubmit(data: any) {
    this.ordonnanceData = data;
  }

  // Lors de la soumission du résumé
  onResumeSubmit(data: string) {
    this.resumeData = data;
  }

  // Soumettre tous les formulaires ensemble
  submitAllForms(): void {
    console.log('malak');
    if (this.consultationForm.valid) {
      console.log('foufou');
      const traitements = this.ordonnanceData?.medications.map((medicament: any) => ({
        nom: medicament.medication,
        dose: medicament.dose,
        consommation: medicament.instructions
      })) || [];

      const examens = this.bilanData?.bilans || [];  // Si les examens ne sont pas définis, initialiser comme tableau vide

      const fullData = {
        nss: this.nss,
        traitements: traitements,
        examens: examens,
        resume: this.resumeData
      };
      console.log('rayane');
      this.consultationservice.submitData(fullData).subscribe({
        next: (response) => {
          console.log('Soumission réussie:', response);
        },
        error: (error) => {
          console.error('Erreur de soumission:', error);
        }
      });
    } else {
      console.error('Un ou plusieurs formulaires ne sont pas remplis.');
    }
  }
}
