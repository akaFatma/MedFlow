import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common'; // Needed for *ngIf

@Component({
  selector: 'app-saisie-bilan1',
  standalone: true, // Assuming this is a standalone component
  imports: [CommonModule], // Import CommonModule for *ngIf
  templateUrl: './saisie-bilan1.component.html',
  styleUrls: ['./saisie-bilan1.component.scss'],
})
export class SaisieBilan1Component implements OnInit {
  bilanId: string | null = null;
  selectedFile: File | null = null;
  previewUrl: string | null = null;

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.bilanId = params['id'];
    });
  }

  triggerFileInput(): void {
    const fileInput = document.getElementById('fileUploader') as HTMLInputElement;
    if (fileInput) {
      fileInput.click();
    }
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (input.files && input.files[0]) {
      this.selectedFile = input.files[0];
      console.log('Selected file:', this.selectedFile);

      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.previewUrl = e.target.result;
      };
      reader.readAsDataURL(this.selectedFile);
    }
  }

  onConfirm(): void {
    if (this.selectedFile) {
      console.log('File ready for upload:', this.selectedFile);
      // Handle file upload logic here
    } else {
      console.log('No file selected.');
    }
  }
}
