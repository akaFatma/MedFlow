import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-bilan',
  imports: [FormsModule, CommonModule],
  templateUrl: './bilan.component.html',
  styleUrls: ['./bilan.component.scss']
})
export class BilanComponent implements OnInit {

  bilans: string[] = [''];

  constructor() {}

  ngOnInit(): void {}

  addBilan(index: number): void {
    if (index === this.bilans.length - 1 && this.bilans[index] !== '') {
      this.bilans.push('');
    }
  }

  trackByIndex(index: number, item: any): number {
    return index;
  }

}