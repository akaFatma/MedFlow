import { Component } from '@angular/core';
import { BilanComponent } from '../../components/bilan/bilan.component';
import { OrdonnanceComponent } from '../../components/ordonnance/ordonnance.component';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
import { ResumeComponent } from '../../components/resume/resume.component';
import { ConsultationHistoryService } from '../../services/consultation-history';
import { ConsultationService } from '../../services/consultation.service';
import { ReactiveFormsModule, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-nouvelle-consultation',
  standalone : true,
  imports: [BilanComponent,OrdonnanceComponent,BienvenuComponentComponent,ResumeComponent , ReactiveFormsModule],
  templateUrl: './nouvelle-consultation.component.html',
  styleUrl: './nouvelle-consultation.component.scss'
})
export class NouvelleConsultationComponent {


  consultationForm: FormGroup;

  constructor(private consultationService: ConsultationService) {
    this.consultationForm = new FormGroup({
      bilan: new FormControl(null, Validators.required),
      ordonnance: new FormControl(null, Validators.required),
      resume: new FormControl('', Validators.required)
    });
  }

  onBilanSubmit(data: any) {
    this.consultationForm.patchValue({ bilan: data });
  }

  onOrdonnanceSubmit(data: any) {
    this.consultationForm.patchValue({ ordonnance: data });
  }

  onResumeSubmit(data: string) {
    this.consultationForm.patchValue({ resume: data });
  }

  submitAllForms(): void {
    if (this.consultationForm.valid) {
      this.consultationService.submitData(this.consultationForm.value).subscribe({
        next: (response) => {
          console.log('Submission successful:', response);
        },
        error: (error) => {
          console.error('Submission error:', error);
        }
      });
    } else {
      console.error('Form is invalid');
    }
  }
}

//   bilanData: any = null;
//   ordonnanceData: any = null;
//   resumeData: string = '';

//   constructor ( private consultationservice : ConsultationService){}

//   //when bilan is submitted 
//   onBilanSubmit(data: any) {
//     this.bilanData = data;
//   }

//   //when l'ordonnance is submitted
//   onOrdonnanceSubmit(data: any) {
//     this.ordonnanceData = data;
//   }

//   //when le resume is submitted
//   onResumeSubmit(data: string) {
//     this.resumeData = data;
//   }

//   //submit all forms together
//   submitAllForms(): void {
//     if (this.bilanData && this.ordonnanceData && this.resumeData) {
//       const fullData = {
//         bilan: this.bilanData,
//         ordonnance: this.ordonnanceData,
//         resume: this.resumeData,
//       };
//     this.consultationservice.submitData(fullData).subscribe({
//     next: (response) => {
//     console.log('Submission successful:', response);
//     },
//     //maybe ill redirect here
//     error: (error) => {
//     console.error('Submission error:', error);
//    }
// });
// } else {
// console.error('One or more forms are not completed.');
// }
//   }


