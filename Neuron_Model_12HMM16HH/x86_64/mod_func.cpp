#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _CaDynamics_E2_reg(void);
extern void _Ca_HVA_reg(void);
extern void _Ca_LVAst_reg(void);
extern void _Ih_reg(void);
extern void _Im_reg(void);
extern void _K_Pst_reg(void);
extern void _K_Tst_reg(void);
extern void _ProbAMPANMDA_EMS_reg(void);
extern void _ProbGABAAB_EMS_reg(void);
extern void _SK_E2_reg(void);
extern void _SKv3_1_reg(void);
extern void _branching_reg(void);
extern void _na12_reg(void);
extern void _na12mut_reg(void);
extern void _na16HH_TF_reg(void);
extern void _na16HHmut_TF_wtcopy_reg(void);
extern void _vclmp_pl_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"mechanisms/CaDynamics_E2.mod\"");
    fprintf(stderr, " \"mechanisms/Ca_HVA.mod\"");
    fprintf(stderr, " \"mechanisms/Ca_LVAst.mod\"");
    fprintf(stderr, " \"mechanisms/Ih.mod\"");
    fprintf(stderr, " \"mechanisms/Im.mod\"");
    fprintf(stderr, " \"mechanisms/K_Pst.mod\"");
    fprintf(stderr, " \"mechanisms/K_Tst.mod\"");
    fprintf(stderr, " \"mechanisms/ProbAMPANMDA_EMS.mod\"");
    fprintf(stderr, " \"mechanisms/ProbGABAAB_EMS.mod\"");
    fprintf(stderr, " \"mechanisms/SK_E2.mod\"");
    fprintf(stderr, " \"mechanisms/SKv3_1.mod\"");
    fprintf(stderr, " \"mechanisms/branching.mod\"");
    fprintf(stderr, " \"mechanisms/na12.mod\"");
    fprintf(stderr, " \"mechanisms/na12mut.mod\"");
    fprintf(stderr, " \"mechanisms/na16HH_TF.mod\"");
    fprintf(stderr, " \"mechanisms/na16HHmut_TF_wtcopy.mod\"");
    fprintf(stderr, " \"mechanisms/vclmp_pl.mod\"");
    fprintf(stderr, "\n");
  }
  _CaDynamics_E2_reg();
  _Ca_HVA_reg();
  _Ca_LVAst_reg();
  _Ih_reg();
  _Im_reg();
  _K_Pst_reg();
  _K_Tst_reg();
  _ProbAMPANMDA_EMS_reg();
  _ProbGABAAB_EMS_reg();
  _SK_E2_reg();
  _SKv3_1_reg();
  _branching_reg();
  _na12_reg();
  _na12mut_reg();
  _na16HH_TF_reg();
  _na16HHmut_TF_wtcopy_reg();
  _vclmp_pl_reg();
}

#if defined(__cplusplus)
}
#endif
