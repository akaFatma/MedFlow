import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SaisieBilanComponent } from './saisie-bilan.component';

describe('SaisieBilanComponent', () => {
  let component: SaisieBilanComponent;
  let fixture: ComponentFixture<SaisieBilanComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SaisieBilanComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SaisieBilanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
