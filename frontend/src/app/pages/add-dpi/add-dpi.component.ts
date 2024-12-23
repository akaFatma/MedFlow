import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';

@Component({
  selector: 'app-add-dpi',
  templateUrl: './add-dpi.component.html',
  styleUrls: ['./add-dpi.component.scss'],
  standalone: true,
  imports: [CommonModule, SidebarComponent],
})
export class AddDPIComponent {
  currentStep: number = 1; // Initialize step to 1

  // Method to move to the next step
  goToNextStep(): void {
    if (this.currentStep < 3) {
      this.currentStep++;
    }
  }

  // Method to move to the previous step
  goToPreviousStep(): void {
    if (this.currentStep > 1) {
      this.currentStep--;
    }
  }
}
