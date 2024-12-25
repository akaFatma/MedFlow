import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { MedicalHistoryComponent } from '../../components/medical-history/medical-history.component';
import { PersonalInfoCardComponent } from '../../components/personal-info-card/personal-info-card.component';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
@Component({
  selector: 'app-consulter-dpipov-patient',
  imports: [MedicalHistoryComponent, PersonalInfoCardComponent, BienvenuComponentComponent],
  templateUrl: './consulter-dpipov-patient.component.html',
  styleUrl: './consulter-dpipov-patient.component.scss'
})
export class ConsulterDPIPovPatientComponent {

}
