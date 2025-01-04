import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SoinsHistoryComponent } from './soins-history.component';

describe('SoinsHistoryComponent', () => {
  let component: SoinsHistoryComponent;
  let fixture: ComponentFixture<SoinsHistoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SoinsHistoryComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SoinsHistoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
