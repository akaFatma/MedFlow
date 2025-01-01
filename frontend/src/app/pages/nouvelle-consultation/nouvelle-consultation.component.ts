// // 
// import { Component } from '@angular/core';
// import { FormBuilder, FormGroup, Validators, FormArray, ReactiveFormsModule } from '@angular/forms';
// import { ConsultationService } from '../../services/consultation.service';
// import { BilanComponent } from '../../components/bilan/bilan.component';
// import { OrdonnanceComponent } from '../../components/ordonnance/ordonnance.component';
// import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
// import { ResumeComponent } from '../../components/resume/resume.component';

// @Component({
//   selector: 'app-nouvelle-consultation',
//   standalone: true,
//   imports: [
//     BilanComponent,
//     OrdonnanceComponent,
//     BienvenuComponentComponent,
//     ResumeComponent,
//     ReactiveFormsModule
//   ],
//   templateUrl: './nouvelle-consultation.component.html',
//   styleUrls: ['./nouvelle-consultation.component.scss']
// })
// export class NouvelleConsultationComponent {
//   consultationForm: FormGroup;

//   constructor(private fb: FormBuilder,
//               private consultationService: ConsultationService) {
//     this.consultationForm = this.fb.group({
//       ordonnance: this.fb.group({
//         date: [{ value: '', disabled: false }, Validators.required],
//         lastName: [{ value: '', disabled: false }, Validators.required],
//         firstName: [{ value: '', disabled: false }, Validators.required],
//         age: [{ value: '', disabled: false }, [Validators.required, Validators.min(0)]],
//         medications: this.fb.array([])
//       }),
//       bilan: this.fb.array([]),
//       resume: [{ value: '', disabled: false }, Validators.required]
//     });
//   }

//   // This method will include disabled controls
//   onSubmit(): void {
//     if (this.consultationForm.valid) {
//       const formData = this.consultationForm.getRawValue(); // Includes disabled fields
//       this.consultationService.submitData(formData).subscribe({
//         next: (response) => console.log('Submission successful:', response),
//         error: (error) => console.error('Submission error:', error)
//       });
//     }
//   }
// }


import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormArray, ReactiveFormsModule } from '@angular/forms';
import { ConsultationService } from '../../services/consultation.service';
import { BilanComponent } from '../../components/bilan/bilan.component';
import { OrdonnanceComponent } from '../../components/ordonnance/ordonnance.component';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
import { ResumeComponent } from '../../components/resume/resume.component';

@Component({
  selector: 'app-nouvelle-consultation',
  standalone: true,
  imports: [
    BilanComponent,
    OrdonnanceComponent,
    BienvenuComponentComponent,
    ResumeComponent,
    ReactiveFormsModule
  ],
  templateUrl: './nouvelle-consultation.component.html',
  styleUrls: ['./nouvelle-consultation.component.scss']
})
export class NouvelleConsultationComponent {
  consultationForm: FormGroup;
 

  constructor(private fb: FormBuilder, private consultationService: ConsultationService) {
    this.consultationForm = this.fb.group({
      ordonnance: this.fb.group({
        date: [{ value: '', disabled: false }, Validators.required],
        lastName: [{ value: '', disabled: false }, Validators.required],
        firstName: [{ value: '', disabled: false }, Validators.required],
        age: [{ value: '', disabled: false }, [Validators.required, Validators.min(0)]],
        medications: this.fb.array([])
      }),
      bilan: this.fb.array([]),
      resume: [{ value: '', disabled: false }, Validators.required]
    });
  }

  onSubmit(): void {
    console.log('Form submit event fired');
    if (this.consultationForm.valid) {
      console.log('Form submit event fired');
      const formData = this.consultationForm.getRawValue(); // Includes disabled fields

      // Debugging: Log the form data to ensure all the fields are being submitted
      console.log('Form Data:', formData);

      this.consultationService.submitData(formData).subscribe({
        next: (response) => console.log('Submission successful:', response),
        error: (error) => console.error('Submission error:', error)
      });
    }
  }
}
