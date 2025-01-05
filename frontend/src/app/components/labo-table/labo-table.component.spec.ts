import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LaboTableComponent } from './labo-table.component';

describe('LaboTableComponent', () => {
  let component: LaboTableComponent;
  let fixture: ComponentFixture<LaboTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LaboTableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LaboTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
