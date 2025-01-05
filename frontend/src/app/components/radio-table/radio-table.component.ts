import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { RadiologueService } from '../../services/radiologue.service';

@Component({
  selector: 'app-radio-table',
  imports: [CommonModule],
  templateUrl: './radio-table.component.html',
  styleUrl: './radio-table.component.scss'
})
export class RadioTableComponent {

errorMessage = '';
  bilans: any;

 constructor(private radiologueService: RadiologueService, private router: Router
  ) {}

  ngOnInit(): void {
    this.loadBilans();
  }

  loadBilans(): void {
    this.radiologueService.getBilans().subscribe({
      next: (data) => {
        this.bilans = data;
        console.log('Soins:', this.bilans);
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching Soins:', error);
      }
    });
  }
  onCompleterBilan(bilanId: string): void {
    this.router.navigate(['/saisie-bilan-radio'], { queryParams: { id: bilanId } });
  }
}
