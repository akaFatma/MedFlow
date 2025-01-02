import { Component, OnInit } from '@angular/core';
import { UserInfoService } from '../../services/personal-info.service';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import {user} from '../../models/user.models'


@Component({
  selector: 'app-personal-info-card',
  imports: [CommonModule],
  templateUrl: './personal-info-card.component.html',
  styleUrl: './personal-info-card.component.scss'
})
export class PersonalInfoCardComponent implements OnInit {
  errorMessage = '';
  decodedQRCode: string = '';
  user : any;
  constructor(
    private userInfoService: UserInfoService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const nss = params['nss'];
      if (nss) {
        this.loadUserInfo(nss);
      }
    });
  }

  loadUserInfo(nss : number): void {
    this.userInfoService.getUserInfo(nss).subscribe({
      next: (data) => {
        this.user = data;
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching user info:', error);
      }
    });
  }



}
