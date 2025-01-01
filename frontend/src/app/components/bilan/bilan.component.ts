// // 
// import { Component, Input } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { FormArray, FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

// @Component({
//   selector: 'app-bilan',
//   standalone: true,
//   imports: [CommonModule, ReactiveFormsModule],
//   templateUrl: './bilan.component.html',
//   styleUrls: ['./bilan.component.scss']
// })
// export class BilanComponent {
//   @Input() parentForm!: FormGroup;
//   isConfirmed = false;

//   constructor(private fb: FormBuilder) {}

//   get bilanArray(): FormArray {
//     return this.parentForm.get('bilan') as FormArray;
//   }

//   addBilan(): void {
//     if (!this.isConfirmed) {
//       this.bilanArray.push(this.fb.control('', Validators.required));
//     }
//   }

//   confirmBilans(): void {
//     this.isConfirmed = true;
//     this.bilanArray.disable(); // Disabling the array so users can't edit after confirmation
//   }

//   trackByIndex(index: number): number {
//     return index;
//   }
// }
import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormArray, FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-bilan',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './bilan.component.html',
  styleUrls: ['./bilan.component.scss']
})
export class BilanComponent {
  @Input() parentForm!: FormGroup;
  isConfirmed = false;

  constructor(private fb: FormBuilder) {}

  get bilanArray(): FormArray {
    return this.parentForm.get('bilan') as FormArray;
  }

  addBilan(): void {
    if (!this.isConfirmed) {
      this.bilanArray.push(this.fb.control('', Validators.required));
    }
  }

  confirmBilans(): void {
    this.isConfirmed = true;
  }

  trackByIndex(index: number): number {
    return index;
  }
}
