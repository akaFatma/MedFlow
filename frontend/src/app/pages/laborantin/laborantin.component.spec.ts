import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LaborantinComponent } from './laborantin.component';

describe('LaborantinComponent', () => {
  let component: LaborantinComponent;
  let fixture: ComponentFixture<LaborantinComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LaborantinComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LaborantinComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
