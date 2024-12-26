import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Output, EventEmitter } from '@angular/core';
import { OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-search-bar',
  imports: [CommonModule , FormsModule],
  templateUrl: './search-bar.component.html',
  styleUrl: './search-bar.component.scss'
})
export class SearchBarComponent {

  searchTerm: number = 0;

  @Output() search: EventEmitter<number> = new EventEmitter<number>();
  @Output() scanQR: EventEmitter<void> = new EventEmitter<void>();

  onSearchChange(value: number): void {
    this.search.emit(value);
  }

  onScanQR(): void {
    this.scanQR.emit();
  }

}
