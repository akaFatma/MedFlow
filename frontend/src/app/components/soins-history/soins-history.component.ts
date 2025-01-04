import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { SoinHistoryService } from '../../services/soin-history.service';
import { Injectable } from '@angular/core';
import { ConsultationPatientService} from '../../services/consult-patient.service';

@Component({
  selector: 'app-soins-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './soins-history.component.html',
  styleUrl: './soins-history.component.scss'
})

export class SoinsHistoryComponent implements OnInit {
  Soins:any;
  errorMessage: string = '';

  @Input() nss: any;
  constructor(private SoinService: SoinHistoryService, private router: Router, 
    private ConsultationPatientService: ConsultationPatientService
  ) {}

  ngOnInit(): void {
    this.loadSoins();
  }

  loadSoins(): void {
    this.SoinService.getSoinHistory(this.nss).subscribe({
      next: (data) => {
        this.Soins = data;
        console.log('Soins:', this.Soins);
        console.log('Data :', data);
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching Soins:', error);
      }
    });
  }

}