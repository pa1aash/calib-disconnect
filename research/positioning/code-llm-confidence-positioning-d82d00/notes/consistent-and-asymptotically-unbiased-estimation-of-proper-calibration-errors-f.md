---
title: Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors
  (full text)
id: consistent-and-asymptotically-unbiased-estimation-of-proper-calibration-errors-f
tags:
- code-llm-confidence-positioning-d82d00
- full-text
created: '2026-11-09T23:28:12.970577Z'
updated: '2026-11-09T23:31:29.318433Z'
source: https://arxiv.org/pdf/2312.08589
status: draft
type: note
content_type: paper
deprecated: false
summary: 'Popordanoska et al. (arXiv 2312.08589): consistent asymptotically unbiased
  estimator of proper calibration errors and refinement, KL calibration error; CIFAR/PreResNet
  experiments; no LLM content.'
---

Consistent and Asymptotically Unbiased Estimation of Proper
                                                                   Calibration Errors



                                                            Teodora Popordanoska∗                             Sebastian G. Gruber∗
                                                                  ESAT-PSI                             German Cancer Research Center (DKFZ)
                                                              KU Leuven, Belgium                         German Cancer Consortium (DKTK)
                                                                                                        Goethe University Frankfurt, Germany




arXiv:2312.08589v1 [cs.LG] 14 Dec 2023
                                                   Aleksei Tiulpin                   Florian Buettner                       Matthew B. Blaschko
                                                  HST Research Unit        German Cancer Research Center (DKFZ)                  ESAT-PSI
                                                  Faculty of Medicine       German Cancer Consortium (DKTK)                  KU Leuven, Belgium
                                               University of Oulu, Finland   Frankfurt Cancer Institute, Germany
                                                                            Goethe University Frankfurt, Germany


                                                               Abstract                               1    Introduction

                                             Proper scoring rules evaluate the quality of             Risk minimization is the cornerstone of machine learn-
                                             probabilistic predictions, playing an essen-             ing, where the goal is to develop models that are accu-
                                             tial role in the pursuit of accurate and well-           rate and provide well-calibrated uncertainty estimates.
                                             calibrated models. Every proper score de-                Central to this pursuit are proper scoring rules (Gneit-
                                             composes into two fundamental components                 ing & Raftery, 2007), which measure the quality of
                                             – proper calibration error and refinement –              probabilistic predictions via dissimilarity measures of
                                             utilizing a Bregman divergence. While un-                probability distributions, known as Bregman diver-
                                             certainty calibration has gained significant             gences (Bregman, 1967; Ovcharov, 2018). A significant
                                             attention, current literature lacks a general            breakthrough in this realm is the decomposition of
                                             estimator for these quantities with known                the expected loss associated with a proper score into
                                             statistical properties. To address this gap,             calibration and refinement (Murphy, 1973; DeGroot &
                                             we propose a method that allows consistent,              Fienberg, 1981; Blattenberger & Lad, 1985; Bröcker,
                                             and asymptotically unbiased estimation of                2009). Facilitated by this result, understanding and
                                             all proper calibration errors and refinement             mitigating calibration error (CE) has become one of the
                                             terms. In particular, we introduce Kullback–             key concerns for applications like healthcare (Haggen-
                                             Leibler calibration error, induced by the com-           müller et al., 2021; Katsaouni et al., 2021), climate
                                             monly used cross-entropy loss. As part of                modelling (Gneiting & Raftery, 2005; Kashinath et al.,
                                             our results, we prove the relation between               2021) and autonomous driving (Yurtsever et al., 2020).
                                             refinement and f-divergences, which implies
                                             information monotonicity in neural networks,             On the most fundamental level, calibration errors com-
                                             regardless of which proper scoring rule is opti-         pare a predictive distribution with a conditional target
                                             mized. Our experiments validate empirically              distribution (Gruber & Buettner, 2022). For this, the
                                             the claimed properties of the proposed estima-           machine learning literature proposed a wide range of
                                             tor and suggest that the selection of a post-hoc         different calibration errors in the multi-class setting
                                             calibration method should be determined by               (Bröcker, 2009; Kull & Flach, 2015; Naeini et al., 2015;
                                             the particular calibration error of interest.            Vaicenavicius et al., 2019; Kumar et al., 2019; Zhang
                                                                                                      et al., 2020; Popordanoska et al., 2022; Gruber & Buet-
                                                                                                      tner, 2022). The most common ones are based on
                                                                                                      absolute or squared differences. However, current liter-
                                                                                                      ature lacks a general estimator of calibration error and
                                         ∗
                                          Shared first authorship. The authors can change the order   refinement induced by any Bregman divergence.
                                         for their own purposes.
                                                                                                      We approach the study of calibration errors through
             Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors

Table 1: Proposed estimators of calibration error and refinement, induced by Brier score (first row) and log loss
                                                                                          \
(second row) for a classifier g, one-hot encoded label y, and dataset size n. The term E[Y | g(xh )] is defined in
Equation (9) via kernel density estimation.

        Loss L (g (x) , y)   Calibration error estimator CE  c F (g)                     Refinement estimator REF
                                                                                                              [ F (g)
                                   n                            2                                 n                2
                       2        1
                                                                                             − n1
                                  P       \                                                       P
          ∥g (x) − y∥2          n      E[Y  | g(x h )] − g(xh )                                      E[Y\| g(xh )]
                                   h=1                                  2                        h=1                  2

                                 n
                                                                                       n D                                   E
                             1                                   \|g(xh )]
                                                 g(xh )], log E[Yg(x              − n1
                                 P            \                                          P        \                  \
         − ⟨log g (x) , y⟩   n             E[Y |                     h)
                                                                                               E[Y | g(xh )], log E[Y | g(xh )]
                                 h=1                                                     h=1



the notion of proper calibration errors (Gruber &                              bounded by the statistical information of the clas-
Buettner, 2022), which is a general class of calibration                       sification task. Based on this result, we derive
errors derived from risk minimization via proper scores.                       the concept of information monotonicity in neural
For example, the Brier score induces the squared L2                            networks beyond mutual information.
calibration error, for which there exists a consistent                      3. We conduct experiments showcasing the empirical
estimator (Popordanoska et al., 2022). Estimating the                          properties of our estimator, as well as its utility
KL calibration error, which is induced by the most                             in selecting an appropriate post-hoc calibration
common proper score in classification – the categorical                        method for the desired calibration error.
negative log likelihood1 remains an open challenge.
In this work, we introduce a consistent and asymptoti-                 2         Related work
cally unbiased estimator for all proper calibration errors
and refinement terms. Additionally, our proposed es-
timator can also be used for estimating the so-called                  In this section, we give a brief overview of estimating
model sharpness. Similar to how every proper score                     calibration errors. Calibration errors are notoriously
generates a proper calibration error, a sharpness term is              difficult to estimate since they compare a prediction
generated. For example, the sharpness induced by the                   g (X) with the conditional expectation E [Y | g (X)],
log loss is the mutual information between prediction                  where Y is the one-hot encoded target variable, X the
and target variable (Huszar, 2013). It is investigated                 input variable, and g the predictive model. The dif-
in the context of general forecasts, but is not well un-               ficulty arises since g (X) is in general a multivariate
derstood for neural networks (DeGroot & Fienberg,                      continuous random variable. Originally, model calibra-
1983; Murphy & Winkler, 1977; Blattenberger & Lad,                     tion was only considered for a finite set of predictions
1985; Bröcker, 2009; Murphy, 1973). We show that any                   (Murphy, 1973), simplifying the estimation since g (X)
model sharpness is identical to an f-divergence (Csiszár,              is then a discrete random variable. Platt (1999) used
1972). Through the information monotonicity of the                     histogram estimation, which transforms the continu-
f-divergence, we then derive the concept of general in-                ous prediction space to a discrete one, to assess the
formation monotonicity in neural networks. This gives                  calibration of a continuous binary model. Different
a novel perspective into the workings of neural networks               ways to define the histogram bins are equal width or
and illustrates how the information bottleneck theory                  equal mass binning techniques (Nguyen & O’Connor,
is a more general concept beyond mutual information.                   2015). The number of bins and the binning scheme
The source codes will be released upon acceptance.                     can significantly influence the estimated value (Kumar
                                                                       et al., 2019) and there is no optimal default since every
Our contributions can be summarized as follows:                        setting has a different bias-variance tradeoff (Nixon
                                                                       et al., 2019). Further, using a fixed binning scheme
 1. We provide a general estimator for all proper cal-                 represents a lower bound of the respective calibration
    ibration errors and refinement in classification,                  error (Kumar et al., 2019; Vaicenavicius et al., 2019).
    which is consistent  and its bias converges with                   In consequence, Vaicenavicius et al. (2019) propose to
    rate O n−1 . In Table 1 we show our derived
                
                                                                       use adaptive binning similar to other approaches in his-
    estimators for calibration error and refinement in-                togram estimation (Nobel, 1996). Roelofs et al. (2022)
    duced by Brier score and log loss.                                 also introduce an algorithm to optimize the number of
 2. We show that model sharpness can be formulated                     bins. Zhang et al. (2020) circumvent binning schemes
    as a multi-distribution f-divergence and is upper                  by using kernel density estimation via Bayes’ theorem.
   1
     We use the terms categorical negative log-likelihood,             The first calibration estimator for a multi-class model
log-loss and cross-entropy loss interchangeably.                       was given by Naeini et al. (2015) and is still the most
                              Popordanoska, Gruber, Tiulpin, Buettner, Blaschko


commonly used measure to quantify calibration, known        Following Ovcharov (2018), the risk related to a proper
as expected calibration error (ECE) (Guo et al., 2017).     loss is connected to a Bregman divergence via
The ECE is a special case of top-label confidence
calibration since it only uses the predicted top-label
confidence maxi∈Y gi (X) and compares it with the           R (g) + E [F (E [Y | X])] = E [DF (E [Y | X] , g (X))] .
conditional accuracy E [YC | maxi∈Y gi (X)] with C =                                                            (2)
arg maxi∈Y gi (X). In contrast, class-wise calibration      Consequently, risk minimization is equivalent to min-
estimation uses all predicted classes, but only in iso-     imizing an expected Bregman divergence since they
lation from each other since it compares gi (X) with        only differ by a model independent constant. The most
E [Yi | gi (X)] for each class i. Both notions depend on    prominent example is the log loss, which induces the
estimating a conditional distribution given a univariate    Kullback–Leibler divergence via the Shannon entropy
continuous random variable. Consequently, estimation        (Ovcharov, 2018).
schemes of one notion can be applied to the other. For
example, Kull et al. (2019) and Nixon et al. (2019) use     We can use Bregman divergences to assess the canonical
histogram binning estimation to estimate class-wise         calibration of a model. Bröcker (2009) showed that
calibration. In contrast, canonical calibration refers to   proper scores in classification can be decomposed into
the case when the model prediction g (X) matches the        calibration and refinement terms. Similarly, we can do
conditional target E [Y | g (X)] almost surely (Vaice-      the same for the risk, namely
navicius et al., 2019; Popordanoska et al., 2022). It is
                                                                     R (g) = E [DF (E [Y | g (X)] , g (X))]
substantially more difficult to estimate with increas-                       |            {z              }
ing classes since g (X) also increases in dimensionality.                              Calibration

This makes histogram based approaches infeasible and                         + E [−F (E [Y | g (X)])] .         (3)
kernel density estimation strongly dependent on the
                                                                               |        {z          }
                                                                                =:REFF (g) (Refinement)
scalability of the kernel to higher dimensions. Popor-
danoska et al. (2022) propose a specific kernel choice
                                                            Gruber & Buettner (2022) defined a calibration error
to estimate canonical Lp calibration errors.
                                                            of the form

3    Proper calibration errors                                     CEF (g) := E [DF (E [Y | g (X)] , g (X))]    (4)

In classification, it is common to use a loss function of   as proper calibration error. Since any convex func-
the form L : ∆k ×Y , where ∆k is the (k−1) dimensional      tion defined on the simplex can be related to a proper
simplex and Y the sample space of the one-hot encoded       score (Ovcharov, 2015), any Bregman divergence can
target variable Y . Further, assume X is the feature        be used to define a proper calibration error. Murphy
variable with realizations in a space X . To optimize       (1973) derived the squared calibration error from the
a model g : X → ∆k mapping from the feature space           Brier score. It is defined as
into the probability simplex, we use the expected loss                           
                                                                                                       2
                                                                                                         
                                                                     CE22 (g) = E E[Y | g(X)] − g(X)      .    (5)
               R (g) := E [L (g (X) , Y )] ,          (1)                                                 2

which is referred to as risk. If L is minimized by
the Bayes classifier g ∗ (x) := E [Y | X = x], then −L      With the square root applied, it is also member of
is a proper score (Gneiting & Raftery, 2007). In            the so-called Lp calibration errors, where the 2-norm
that case, we may also refer to L as a proper loss          is replaced by a general p-norm (Naeini et al., 2015;
(Williamson, 2014). The best achievable (negative)          Kumar et al., 2019; Wenger et al., 2020; Popordanoska
risk for a given target distribution q is given by          et al., 2022). Popordanoska et al. (2022) propose an
F (q) := − inf p∈∆k EY ∼q [L (p, Y )]. The function F       estimator of Lp calibration errors via kernel density
is convex if and only if −L is a proper score (Gneiting     estimation and offer evaluations of the squared calibra-
& Raftery, 2007).                                           tion error. Another example of a proper calibration
                                                            error can be derived from the log-likelihood and results
Every differentiable proper score is uniquely associated    in a calibration error based on the Kullback–Leibler
with a Bregman divergence. A Bregman divergence             divergence DKL given by
(Bregman, 1967) in a k-dimensional space U ⊂ Rk is
characterized by a continuously differentiable, strictly           CEKL (g) = E [DKL (E[Y | g(X)], g(X))] .     (6)
convex function F : U → R, with DF (p, q) := F (p) −
F (q) − ⟨∇F (q), p − q⟩. Special cases are the squared      As all differentiable proper calibration errors are in-
Euclidean distance with F (p) = ∥p∥22 , and the Kullback–   duced by a Bregman divergence, non-negativity ap-
                                 Pk
Leibler divergence with F (p) = i=1 pi log (pi ).           plies immediately, but the range is dependent on
             Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors


which divergence is employed: CE22 (g) ∈ [0, 2], while            where a natural choice for k can be the Dirichlet kernel
CEKL (g) ∈ [0, ∞). Since we are only using distribu-              (Popordanoska et al., 2022), defined as
tions as inputs for calibration errors, the Kullback–
                                                                                               PK          K
Leibler CE is more principled according to information                                       Γ( k=1 αjk ) Y         α −1
theory than the squared calibration error (MacKay,                   kDir (g(xi ), g(xj )) = QK               g(xi )k jk
                                                                                               k=1 Γ(α   )
                                                                                                       jk k=1
2003). The squared error implies a Euclidean geometry
                                                                                                                         (10)
for its inputs since the input space is non-bounded.                         g(xj )
But, distributions are non-negative and normalized,               with αj = h +1 (Ouimet & Tolosana-Delgado, 2022).
and, consequently, exist in a bounded space. The                  This results in a differentiable, asymptotically unbiased
Kullback–Leibler divergence is a better representation            and consistent estimator of the conditional expectation.
of these restrictions since it is also not defined for neg-       Another common choice for estimating the conditional
ative inputs (MacKay, 2003). Currently, no estimator              expectation is by using a binning kernel (which returns
for general proper calibration errors exist, including the        1 if g(xi ) and g(xj ) fall in the same bin, and 0 other-
Kullback–Leibler case. As part of this work we propose            wise), resulting  in an estimator given by E[Y\     | g(X)] =
a consistent, asymptotically unbiased and differentiable              1
                                                                            P
                                                                                       y  , where B         denotes the bin into
                                                                  |Bg(x ) |   j∈Bg(x )  j           g(x h )
estimator for any proper calibration error.                             h           h
                                                                  which g(xh ) is assigned. Although this approach allows
                                                                  for faster computation, the estimator is not differen-
4    Estimating proper calibration errors                         tiable, thus preventing it to be directly used as part of
                                                                  calibration regularized training or differentiable recal-
Given an i.i.d. labeled data sample {(xi , yi )}1≤i≤n , a         ibration methods. In addition, several papers (Vaice-
generic Bregman divergence calibration error estimator            navicius et al., 2019; Widmann et al., 2019; Ashukha
can be defined via                                                et al., 2020) have raised concerns about asymptotic in-
              n
                                                                  consistency of binned estimators, as well as sensitivity
            1X               
                                                                  to the binning scheme, and limited scalability with the
CEF (g) ≈       F E[Y\
                     | g(xh )] − F (g(xh ))              (7)
            n                                                     number of classes.
              h=1
                                                             !
                     D                                     E
                                       \
                    − ∇F (g(xh )) , E[Y | g(xh )] − g(xh )    .5        Statistical properties

It is straightforward to verify that the application of           We show here the existence of consistent and asymp-
F (x) = ∥x∥22 recovers exactly the L2 special case of             totically unbiased estimators of arbitrary proper cali-
the estimator given by (Popordanoska et al., 2022,                bration errors. We first show in Section 5.1 that the
Equation (9)), while setting F (p) = ⟨p, log(p)⟩ yields           optimal big-O convergence rates for estimators of CEF
                                                                  and REFF are the same and that a consistent estimator
             n
               *
                                            \
                                                         !+       of one can be used to construct an estimator of the
           1X                            E[Y | g(xh )]
CEKL (g) ≈       E[Y\
                    | g(xh )], log                            ,   other. We then prove in Section 5.2 via a Taylor series
           n                                g(xh )                approach that an estimator via REFF gives asymptotic
              h=1
                                                         (8)      unbiasedness for all Bregman divergences, giving a con-
                                                                  structive proof that a single software implementation
where log and division operations are taken element-              can provide a good baseline estimator for any proper
wise, and we may interpret the inner product using                calibration error using a function reference for F to
limy↘0 y log y = 0 to ensure that it remains well defined         parameterize the Bregman divergence.
on the vertices of the probability simplex. Detailed
derivations of calibration error and refinement estima-
                                                                  5.1       Estimation via refinement
tors are in Appendix D. In the sequel, our notation
will use capital letters for unbounded random variables,          Equation (7) provides a calibration error estimate di-
and lower case variables with subscripts for elements of          rectly from the definition of a Bregman divergence, but
our data sample. Note that we may still treat elements            we show here that we can also use an estimate based on
of the data sample as random variables.                           refinement using the decomposition (cf. Equation (49))
We define the finite sample estimator for the condi-
tional expectation as in Popordanoska et al. (2022,               E [DF (Y, g(X))] − CEF (g) = E[F (Y ) − F (E[Y | g(X)])].
Equation (3))                                                                                                       (11)
                       Pn                                         From this decomposition and that E [DF (Y, g(X))] can
                        j=1 k(g(X), g(xj ))yj
          \
       E[Y | g(X)] := Pn                      ,  (9)              be estimated with an empirical average achieving an
                         j=1 k(g(X), g(xj ))                      unbiased estimator with O(n−1/2 ) rate of convergence,
                               Popordanoska, Gruber, Tiulpin, Buettner, Blaschko


we see that the difficulty of estimating refinement or            When D2 F (E[Y | g(xh )]) ̸= 0, this yields
CE is essentially the same, as the rate of bias and con-
                                                                        E ∆T D2 F (E[Y | g(xh )]) ∆
                                                                                                     
vergence for an estimator of one can be transferred to
the other by subtracting from the empirical estimate                            h                   i
                                                                        ≍ Trace Cov E[Y\    | g(xh )]
of the risk. Furthermore, we note that a simple empiri-
cal mean over {F (yi )}1≤i≤n is the Minimum-Variance                           h             i                2        (15)
                                                                          + E E[Y\  | g(xh )] − E[Y | g(xh )] ,
Unbiased Estimator (MVUE) of E[F (Y )] for a finite
sample, and it is the estimate of −E[F (E[Y | g(X)])]
                                                                            |                {z              }
                                                                                                     2
                                                                                 = Bias E[Y\
                                                                                           |g(xh )]       =O(n−2 )
that is the primary challenge.
To summarize, assuming an empirical estimator of the              where the notation ≍ is taken here to mean that the
                               [ F (g) ≈ E[−F (E[Y |
refinement (cf. Equation (13)) REF                                left and right side have the same asymptotic rate
g(X)])], we may compute                                           of convergence in n, and the r.h.s. is due to a bias-
                                                                  variance decomposition of the l.h.s. Finally, we have
                          n
                                                                                    
                       1X                                         Var E[Y |\ g(xh )]i = O(n−1 ), which implies
CEF (g) := − [
c           REFF (g) +       (DF (yi , g(xi )) − F (yi )) ,
                       n i=1
                                                                                            
                                                           (12)                       [ F (g) = O(n−1 )
                                                                                Bias REF                               (16)

and the rates of convergence of CEc F (g) and its bias
                                                                  irrespective of F . We therefore conclude that estima-
will be determined by the rates of REF
                                   [ F (g).                       tion of any proper calibration error via Equation (12)
                                                                  results in a consistent and asymptotically unbiased
5.2     Asymptotic unbiasedness and rate of bias                  estimator with convergence O(n−1/2 ), and bias that
                                                                  converges as O(n−1 ).
If we use the empirical estimator of E[Y | g(X)] in
Equation (9), the bias converges as O(n−1 ) while the
estimator itself has a rate of O(n−1/2 ). By the same
                                                                  6     Relationship with information
argument as Gruber & Buettner (2022, Footnote 2),                       monotonicity in neural networks

                                                                  A key part of this work is to relate uncertainty cali-
                      n       P                            !
               1X               j̸=h k(g(xh ), g(xj ))yj
 REFF (g) := −
 [                F            P                                  bration to information theoretic principles. First, we
               n                  j̸=h k(g(xh ), g(xj ))
                     h=1                                          summarize relevant concepts and provide the necessary
                                                           (13)   foundation to derive our contributions.
is a consistent and asymptotically unbiased estimator
of the refinement E[−F (E[Y | g(X)])] for all F . We              6.1   Background on information monotonicity
note that continuity of F , a condition required for the
                                                                  In machine learning, information monotonicity is most
argument of Gruber & Buettner (2022, Footnote 2), is
                                                                  commonly known through the information bottleneck
guaranteed for all Bregman divergences as F is differ-
                                                                  theory (Slonim & Tishby, 1999; Bialek et al., 2001;
entiable by assumption.
                                                                  Gilad-Bachrach et al., 2003; Chechik et al., 2003;
                                           REFF (g)
We now show the asymptotic rate of bias of [                      Shamir et al., 2010; Shwartz-Ziv & Tishby, 2017; Saxe
using a Taylor series expansion. First, define ∆ =                et al., 2018). Information monotonicity states that each
E[Y\ | g(xh )] − E[Y | g(xh )]. The rate of bias of               layer in a neural network is indirectly optimized by the
                                                                  mutual information of the output, resulting in a so-
REFF (g) is determined by the rate of bias of each
[
                                                                  called information flow, or information plane dynamics,
of the summands in Equation (13)
                                                                  throughout the network (Saxe et al., 2018; Goldfeld
   h              i                                             et al., 2019).
  E F E [Y\
          | g(xh )] = E [F (E[Y | g(xh )] + ∆)]
                                                                  Further, Csiszár (1972) derived the class of f-
      ≈ F (E[Y | g(xh )]) + E [D F (E[Y | g(xh )]) ∆]             divergences according to several principles, including in-
                                        
              1 T 2                                               formation monotonicity. These divergences between dis-
        + E ∆ D F (E[Y | g(xh )]) ∆ + . . .           (14)        tributions are widely applicable, for example through-
              2
                                                                  out statistics (Liese & Vajda, 2006) and in generative
where D is the differential operator. It is well known            modelling (Creswell et al., 2018). Similar to Garcia-
that the bias of the 1st order term (a ratio estimator)           Garcia & Williamson (2012) and Duchi et al. (2018), we
is O(n−1 ) and the remaining bias will be dominated               use the following definition for multiple distributions.
                                                                                                       k
by the 2nd order term (Wolter, 2007, Theorem 6.2.5).              Given a convex function f : [0, ∞) → (−∞, ∞] with
                 Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors


f (1, . . . , 1) = 0, the f-divergence between distribu-                  distributions and the marginal prediction distribution.
tions P1 , . . . , Pk and Q is defined by                                 The marginal class distribution determines the weight
                            Z                                           of each ratio. For a given classification task, it is
                                   dP1       dPk                          constant across all models. We can now provide the
  If (P1 , . . . , Pk ∥ Q) = f         ,...,       dQ. (17)
                                   dQ        dQ                           key result of this section.
Following the property of f ,              we have                        Theorem 6.2 (Information monotonicity in neural net-
If (P1 , . . . , Pk ∥ Q) ≥   0 with equality if                           works). For a neural network g (X) = hl (. . . (h1 (X)))
P1 = · · · = Pk = Q. Let M be a Markov ker-                               with layers hi , i ∈ {1, . . . , l}, conditional distributions
nel transforming a distribution P into a distribution                     Pyi := P (hi (. . . (h1 (X))) | Y = y), and marginal dis-
                                                                                                 
M P , then Garcia-Garcia & Williamson (2012) show                         tributions P i := E PYi , we have
that the information monotonicity is given by
                                                                              SHARPF (g) = IF Y P1l , . . . , Pkl ∥ P l
                                                                                                                          
   If (M P1 , . . . , M Pk ∥ M Q) ≤ If (P1 , . . . , Pk ∥ Q) .
                                                                                             ≤ IF Y P1l−1 , . . . , Pkl−1 ∥ P l−1
                                                                                                                                   
                                                                                                                                        (22)
                                                            (18)
                                                                                             ≤ · · · ≤ IF Y P11 , . . . , Pk1 ∥ P 1 .
                                                                                                                                   
In the following, we make the novel connection between
f-Divergences and refinement via model sharpness. The
sharpness of a model is defined via (DeGroot & Fien-                      This theorem offers a generalization of the information
berg, 1981)                                                               flow in neural networks. Since sharpness is optimized
                                                                          towards the maximum during model training, the infor-
    SHARPF (g) = E [DF (E [Y | g (X)] , E [Y ])] .                (19)    mation (as quantified by an f-divergence) is implicitly
                                                                          maximized in each layer no matter the proper loss.
If F is the Shannon entropy, then the sharpness is                        The signal, which is forward propagated in each layer,
equivalent to the mutual information between output                       follows the known information flow of the information
variable and target variable. Model sharpness is related                  bottleneck theory. A rich literature exists on informa-
to the refinement term (DeGroot & Fienberg, 1981,                         tion bottleneck experiments (Shwartz-Ziv & Tishby,
1983; Kull & Flach, 2015; Kuleshov & Deshpande, 2022)                     2017; Saxe et al., 2018; Goldfeld et al., 2019; Wu &
by                                                                        Fischer, 2020; Wu et al., 2020; Wang et al., 2022). In
                                                                          Section 7 we will extend on that by monitoring the
 − SHARPF (g) = F (E [Y ]) + E [−F (E [Y | g (X)])] .                     model sharpness via the refinement term throughout
                             |        {z          }
                                                (Refinement)              model training and by assessing information monotonic-
                                                 (20)                     ity beyond mutual information.
Consequently, we can use our proposed refinement esti-
                                                                          In Section 2, we have seen that calibration and sharp-
mator for calibration and sharpness.
                                                                          ness are two different yet related concepts derived from
                                                                          risk minimization. Theorem 6.2 presents a novel link
6.2     A novel generalization of neural network                          between information bottleneck theory and uncertainty
        information monotonicity                                          calibration – two key research areas in deep learning,
                                                                          which consist of rich literature but little exchange. For
We now present our contribution regarding the exis-
                                                                          example, according to our result, optimizing via the
tence of information monotonicity in neural networks.
                                                                          information bottleneck theory does not offer calibrated
As a preliminary step, we first show that model sharp-
                                                                          predictions and requires post-hoc uncertainty calibra-
ness has the form of an f-divergence. We defer proofs
                                                                          tion for trustworthy probability forecasts. This under-
to Appendix B.
                                                                          lines the general importance of calibration estimation.
Proposition 6.1 (Sharpness as f-divergence). Let
F : ∆k → R be a convex function and g : X →
∆k a classifier with prediction distributions Py :=                       7     Experiments
P (g (X) | Y = y), and P := P (g (X)). Then, the
model sharpness can be represented as an f-divergence                     The outline of the experiments is as follows. We (i) com-
via                                                                       pare the choices of kernel for the conditional expecta-
        SHARPF (g) = IF Y (P1 , . . . , Pk ∥ P ) , (21)                   tion estimator, discussed in Section 4; (ii) compare the
                                                                          direct estimator from Equation (7) with the estimator
where F Y (x)             :=     F (E [Y1 ] x1 , . . . , E [Yk ] xk ) −   derived via risk in Equation (12); (iii) analyse the em-
F (E [Y1 ] , . . . , E [Yk ]).                                            pirical properties of the proposed estimator, derived in
                                                                          Section 5.1; (iv) show new insights regarding the choice
Thus, we can interpret the classifier sharpness as the                    of post-hoc calibration method, depending on the cho-
f -Divergence between the class-conditional prediction                    sen calibration error; (v) demonstrate the information
                                      Popordanoska, Gruber, Tiulpin, Buettner, Blaschko

                                                                                                            0.08
                            Ground truth                                     Ground truth                                           2 classes
        0.15                CE
                            c KL (Dirichlet)                                                                                        5 classes
                                                          0.08               CEKL via risk
                                                                             c
                                                                                                            0.06                    10 classes
                            CE
                            c KL (Binning)

                                                                                                CEKL bias
                                                                             CEKL direct
                                                                             c

 CEKL                                              CEKL                                                     0.04
                                                   c
         0.1                                              0.06

                                                                                                            0.02
        0.05                                              0.04
                                                                                                              0
                 0         5000            10000                 0        5000          10000                      0         5000          10000
                      Number of points                               Number of points                                   Number of points
               (a) Dirichlet vs. Binning             (b) Direct vs. estimation via risk                            (c) Bias convergence

Figure 1: (a) A comparison of the binning-based estimator and the KDE-based estimator with Dirichelt kernel. (b)
A comparison of the CE estimator using Equation (12) and direct estimation via Equation (7). (c) Convergence
of the bias as a function of the number of points used for the estimation.


monotonicity in neural networks, discussed in Section                     cally the direct implementation (orange) performs even
6.2, for the L2 case via our proposed estimator.                          better. Finally, Figure 1c shows the convergence of the
                                                                          bias of CE
                                                                                  c KL as a function of the number of points used
In all experiments we evaluate class-wise CE, which
                                                                          for the estimation. We observe that regardless of the
can be derived from One-vs-Rest risk minimization
                                                                          number of classes, the estimator consistently provides
(c.f. Appendix C). The CE estimator obtained by
                                                                          reliable estimates of class-wise calibration error.
setting F (x) = ∥x∥22 in Equation 12 will be denoted
    d2 , while the one derived from F (p) = ⟨p, log(p)⟩
as CE     2                                                               7.2     Post-hoc calibration
will be referred to as c CEKL . The bandwidth of the
Dirichlet kernel is determined through a combination                      Here we demonstrate the application of our
of a leave-one-out maximum likelihood estimation and                      proposed estimator for evaluating CE on CI-
visual inspection of the resulting density. Typical values                FAR10/100 (Krizhevsky & Hinton, 2009), after per-
range from 0.01 to 0.0001.                                                forming post-hoc calibration. Following standard prac-
                                                                          tice, we trained various PreResNet (He et al., 2016),
                                                                          VGG16 (Simonyan & Zisserman, 2014) and WideRes-
7.1       Empirical properties
                                                                          Net (Zagoruyko & Komodakis, 2016) architectures. De-
                                                                          tails about the training can be found in Appendix E.
To analyze the empirical properties of the proposed
estimator, we create synthetic data with miscalibrated                    In Table 2 we present a comparison of c CEKL and CE  d2
                                                                                                                                 2
scores, for which the ground truth CE is known, fol-                      for models before and after calibration with temper-
lowing Popordanoska et al. (2022). First, we sample                       ature scaling (TS) and isotonic regression (IR) (Guo
uniform points from the simplex and we apply temper-                      et al., 2017). We focus on these methods because of
ature scaling with t1 = 0.9 to ensure that the scores                     their distinct optimization objectives during calibra-
are closer to the boundaries of the simplex. Then, we                     tion: TS minimizes the NLL loss, while IR aims to
generate ground truth labels based on the sampled prob-                   optimize a weighted Brier score. It is notable that we
abilities, resulting in a perfectly calibrated classifier.                obtain a much better c  CEKL score with TS across all
Finally, to intentionally introduce miscalibration, we                    architectures on both datasets. For instance, we report
apply an additional temperature scaling with t2 = 0.6.                    42% improvement from the uncalibrated score using
In Figure 1a we compare the performance of two pro-                       TS, compared with 24% decrease in CE using IR for
posed choices of kernel, kDir and kbin , for increasing                   PreResNet164 on CIFAR-10. The effect is opposite for
number of samples used for the estimation. We observe                      d2 : IR is a better suited calibration technique if one
                                                                          CE  2
that the Dirichlet-based estimator not only has better                    aims to minimize this metric. For example, calibration
properties, like differentiability, consistency and asymp-                with IR on VGG16BN results in 42% decrease in CE,
totic unbiasedness, but also has better empirical perfor-                 compared to only 20% decrease with TS. On the other
mance. Figure 1b compares the direct implementation                       hand, if the goal is to optimize CE
                                                                                                           c KL , the results on
of the estimator, as given in Equation (7), with the                      CIFAR-100 indicate that IR may even harm this metric.
estimator derived via the risk, given in Equation (12).                   Table 3 summarizes the accuracy on CIFAR-10 before
We derived theoretically the statistical properties of the                and after calibration with IR. We notice that while
estimator in Equation (12) (blue curve), and empiri-                      TS is known to be accuracy-perserving, IR also retains
              Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors


                                  c KL × 100 and CE
Table 2: Performance evaluation (CE                d2 × 100, lower is better) of various network architectures on
                                                     2
CIFAR-10/100 with no calibration, and after recalibrating with IR and TS. The number in the bracket represents
the change of CE (in %) relative to the uncalibrated score. The results are averaged over 5 seeds.

                                     No calibration                 Isotonic regression                                     Temperature scaling
   Dataset          Model            CEKL
                                     c         d2
                                               CE                  CEKL
                                                                   c                 d2
                                                                                     CE                                    CEKL
                                                                                                                           c                d2
                                                                                                                                           CE
                                                  2                                     2                                                     2

                PreResNet20      2.74±0.06   1.12±0.01    1.57±0.05 (↓ 43%)                  0.58±0.01 (↓ 48%)       1.26±0.02 (↓ 54%)              0.66±0.01 (↓ 41%)
                PreResNet56      1.94±0.04   0.84±0.03    1.30±0.03 (↓ 33%)                  0.50±0.03 (↓ 41%)       1.03±0.02 (↓ 47%)              0.54±0.02 (↓ 36%)
                PreResNet110     1.76±0.03   0.77±0.01    1.26±0.03 (↓ 29%)                  0.49±0.01 (↓ 37%)       0.98±0.01 (↓ 44%)              0.51±0.01 (↓ 33%)
  CIFAR-10
                PreResNet164     1.58±0.02   0.70±0.01    1.20±0.02 (↓ 24%)                  0.43±0.02 (↓ 38%)       0.91±0.02 (↓ 42%)              0.47±0.01 (↓ 32%)
                  VGG16BN        2.85±0.05   1.00±0.02    1.36±0.03 (↓ 52%)                  0.57±0.01 (↓ 42%)       1.38±0.03 (↓ 52%)              0.80±0.02 (↓ 20%)
               WideResNet28x10   1.21±0.02   0.61±0.01    1.09±0.03 (↓ 10%)                  0.41±0.01 (↓ 34%)       0.93±0.01 (↓ 23%)              0.49±0.01 (↓ 19%)
                PreResNet20      0.76±0.01   0.38±0.00    0.96±0.02 (↑ 26%)                  0.35±0.00 (↓ 9%)         0.70±0.00 (↓ 8%)               0.35±0.00 (↓ 8%)
                PreResNet56      0.78±0.02   0.35±0.01    0.88±0.01 (↑ 13%)                  0.28±0.00 (↓ 21%)       0.61±0.01 (↓ 22%)              0.30±0.00 (↓ 14%)
                PreResNet110     0.76±0.01   0.34±0.00    0.85±0.01 (↑ 12%)                  0.27±0.00 (↓ 20%)       0.60±0.00 (↓ 21%)              0.30±0.00 (↓ 12%)
 CIFAR-100
                PreResNet164     0.74±0.00   0.33±0.00    0.86±0.01 (↑ 16%)                  0.26±0.00 (↓ 21%)       0.59±0.01 (↓ 20%)              0.29±0.00 (↓ 11%)
                  VGG16BN        1.23±0.01   0.43±0.00    0.95±0.01 (↓ 23%)                  0.34±0.00 (↓ 21%)       0.75±0.00 (↓ 39%)              0.38±0.00 (↓ 11%)
               WideResNet28x10   0.62±0.01   0.30±0.00    0.72±0.02 (↑ 15%)                  0.22±0.00 (↓ 27%)        0.60±0.01 (↓ 3%)               0.30±0.00 (↓ 1%)



             Table 3: Accuracy on CIFAR-10.                            We train a fully connected neural network on MNIST
                                                                       via stochastic gradient descent. The model has four
       Model          No calibration     Isotonic regression           hidden layers with nine nodes each. In Figure 2, we
   PreResNet20          91.95±0.05           91.94±0.07                show that the model accuracy and L2 sharpness of
   PreResNet56          94.38±0.13           94.34±0.13                each intermediate layer throughout training. Note that
   PreResNet110         94.86±0.04           94.83±0.05                sharpness can also be interpreted as mutual informa-
   PreResNet164         95.24±0.05           95.14±0.06                tion. At the beginning of training, the information in
     VGG16BN            93.26±0.04           93.23±0.04                each layer increases sharply similar to the accuracy.
  WideResNet28x10       95.54±0.05           95.53±0.04
                                                                       But, the initial increase of information holds no longer
                                                                       for layers one and two, while layers three and four
                                                                       experience a slow-down in information gain. This in-
accuracy in practice for this setting. In summary, these               formation gap is then reduced for longer periods of
findings suggest that the choice of calibration method                 training. We conclude that the information in each
should be influenced by the specific calibration error of              layer is not optimized uniformly throughout training,
                                                    d2 ,
interest, i.e., IR is more suitable for minimizing CE                  which can be monitored via our refinement estimator.
                                                               2
whereas TS should be preferred for CE
                                   c KL .                                                                                                 0.8
                                                                                    80
The full table evaluating accuracy, NLL and Brier score                                                                                   0.6


                                                                         Accuracy                                          L2 Sharpness
                                                                                    60
is in Appendix E. Additional experiments involving con-                                                                                   0.4
vergence of bias, monitoring CE and sharpness during                                40                                                                                Layer 1
training, performing model selection, and measuring                                                                                       0.2                         Layer 2
                                                                                    20                                                                                Layer 3
class-wise CE are also discussed in that Appendix.                                                                                         0
                                                                                                                                                                      Layer 4
                                                                                         0         10           20    30                        0   10           20         30
                                                                                                        Epoch                                            Epoch
7.3   Information monotonicity
                                                                       Figure 2: Accuracy and information monotonicity
We illustrate the information monotonicity in neural                   throughout training via our sharpness estimator (here:
networks via our refinement estimator. We can apply                    L2 ). Each consecutive layer’s sharpness is lower
our refinement estimator also to the sharpness of                      bounded by the next layer. The sharpness of the whole
random vectors not located in the simplex. For this,                   model is optimized implicitly via a proper score.
note that E [f (E [Y | X])] = E [f (E [Y | g (X)])] for
any function f and injective function g (c.f. Appendix
D.8 in (Gruber & Buettner, 2022)). In our case, f                      8                 Discussion and conclusions
is the convex function of a refinement term and g
is chosen to be an invertible version of the softmax                   In this paper, we proposed a consistent and differen-
function and X are the activations of an intermediate                  tiable estimator for all proper calibration errors. The
layer.                                                                 estimator is asymptotically unbiased, has a conver-
                                                                       gence rate of O(n−1/2 ), and the bias decreases at a
                              Popordanoska, Gruber, Tiulpin, Buettner, Blaschko


rate of O(n−1 ). Specifically, we introduce the Kullback–
Leibler CE as a theoretically justified choice in stan-
dard neural network training procedures that utilize
log loss. Furthermore, we showed that model sharpness,
a generalization of mutual information, is equal to a
multi-distribution f-divergence. Via this relation, we
proved that information monotonicity in neural net-
works is a general concept beyond log minimization and
can be monitored via sharpness during model training.
Our work has several limitations. It is an open research
question to find bias corrections for proper CE estima-
tors. Although Popordanoska et al. (2022) provided a
                       d2 , it does not transfer directly
debiasing strategy for CE 2
to our more general case. Further, an intrinsic problem
of density estimators for CE is the O(n2 ) complexity.
In our experiments, we demonstrate that evaluation
can be effectively computed on subsets of reasonable
size. However, assessing larger sets becomes compu-
tationally expensive. Improved debiasing could make
block estimators feasible (Zaremba et al., 2013), leading
also to improved computational properties.
In summary, we show that there exist asymptotically
unbiased estimators for an entire landscape of proper
CEs. The experimental results demonstrate the empiri-
cal behavior of the proposed approach and showcase its
properties in assessing CE and sharpness. This makes
it a valuable component for designing calibration meth-
ods which aim to minimize a specific CE.

Acknowledgements

This research received funding from the Flemish Gov-
ernment (AI Research Program) and the Research
Foundation - Flanders (FWO) through project number
G0G2921N. The publication was also supported by
funding from the Academy of Finland (Profi6 336449
funding program), the University of Oulu strategic
funds, the Wellbeing Services County of North Os-
trobothnia (VTR project K62716), Terttu Foundation,
and the Finnish Foundation for Cardiovascular Re-
search. The authors wish to acknowledge CSC – IT
Center for Science, Finland, for generous computational
resources.
Co-funded by the European Union (ERC, TAIPO,
101088594 to FB). Views and opinions expressed are
however those of the authors only and do not necessar-
ily reflect those of the European Union or the European
Research Council. Neither the European Union nor the
granting authority can be held responsible for them.
             Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors


References                                                      Gneiting, T. and Raftery, A. E. Strictly proper scoring rules,
                                                                  prediction, and estimation. Journal of the American
Ashukha, A., Lyzhov, A., Molchanov, D., and Vetrov, D.           Statistical Association, 102(477):359–378, 2007. doi: 10.
  Pitfalls of in-domain uncertainty estimation and ensem-        1198/016214506000001437.
  bling in deep learning. In International Conference on
  Learning Representations, 2020.                               Goldfeld, Z., Van Den Berg, E., Greenewald, K., Melnyk, I.,
                                                                  Nguyen, N., Kingsbury, B., and Polyanskiy, Y. Estimat-
Bialek, W., Nemenman, I., and Tishby, N. Predictability,          ing information flow in deep neural networks. In 36th
  complexity, and learning. Neural computation, 13(11):           International Conference on Machine Learning, ICML
  2409–2463, 2001.                                                2019, pp. 4153–4162. International Machine Learning
Blattenberger, G. and Lad, F. Separating the brier score          Society (IMLS), 2019.
  into calibration and refinement components: A graphical       Gruber, S. G. and Buettner, F. Better uncertainty cali-
  exposition. The American Statistician, 39(1):26–32, 1985.       bration via proper scores for classification and beyond.
Bregman, L. The relaxation method of finding the common           In Oh, A. H., Agarwal, A., Belgrave, D., and Cho, K.
  point of convex sets and its application to the solution of    (eds.), Advances in Neural Information Processing Sys-
  problems in convex programming. USSR Computational              tems, 2022.
  Mathematics and Mathematical Physics, 7(3):200 – 217,         Guo, C., Pleiss, G., Sun, Y., and Weinberger, K. Q. On
  1967. ISSN 0041-5553. doi: https://doi.org/10.1016/            calibration of modern neural networks. In International
  0041-5553(67)90040-7.                                          Conference on Machine Learning, pp. 1321–1330. PMLR,
Bröcker, J. Reliability, sufficiency, and the decomposition      2017.
  of proper scores. Quarterly Journal of the Royal Mete-        Gupta, A., Kvernadze, G., and Srikumar, V. Bert & family
  orological Society, 135(643):1512–1519, Jul 2009. ISSN          eat word salad: Experiments with text understanding.
  1477-870X. doi: 10.1002/qj.456.                                ArXiv, abs/2101.03453, 2021.
Chechik, G., Globerson, A., Tishby, N., and Weiss, Y.           Gupta, K., Rahimi, A., Ajanthan, T., Mensink, T., Smin-
  Information bottleneck for Gaussian variables. Advances         chisescu, C., and Hartley, R. Calibration of neural net-
 in Neural Information Processing Systems, 16, 2003.             works using splines. In International Conference on
Creswell, A., White, T., Dumoulin, V., Arulkumaran, K.,          Learning Representations, 2020.
  Sengupta, B., and Bharath, A. A. Generative adversarial       Haggenmüller, S., Maron, R. C., Hekler, A., Utikal, J. S.,
  networks: An overview. IEEE signal processing magazine,         Barata, C., Barnhill, R. L., Beltraminelli, H., Berking,
  35(1):53–65, 2018.                                              C., Betz-Stablein, B., Blum, A., Braun, S. A., Carr, R.,
Csiszár, I. A class of measures of informativity of observa-      Combalia, M., Fernandez-Figueras, M.-T., Ferrara, G.,
  tion channels. Periodica Mathematica Hungarica, 2(1-4):         Fraitag, S., French, L. E., Gellrich, F. F., Ghoreschi, K.,
  191–213, 1972.                                                  Goebeler, M., Guitera, P., Haenssle, H. A., Haferkamp,
                                                                  S., Heinzerling, L., Heppt, M. V., Hilke, F. J., Hobels-
DeGroot, M. H. and Fienberg, S. E. Assessing probability          berger, S., Krahl, D., Kutzner, H., Lallas, A., Liopyris, K.,
  assessors: Calibration and refinement. Technical report,        Llamas-Velasco, M., Malvehy, J., Meier, F., Müller, C. S.,
  CARNEGIE-MELLON UNIV PITTSBURGH PA DEPT                         Navarini, A. A., Navarrete-Dechent, C., Perasole, A.,
  OF STATISTICS, 1981.                                            Poch, G., Podlipnik, S., Requena, L., Rotemberg, V. M.,
DeGroot, M. H. and Fienberg, S. E. The comparison and             Saggini, A., Sangueza, O. P., Santonja, C., Schadendorf,
  evaluation of forecasters. Journal of the Royal Statistical     D., Schilling, B., Schlaak, M., Schlager, J. G., Sergon,
  Society. Series D (The Statistician), 32(1/2):12–22, 1983.      M., Sondermann, W., Soyer, H. P., Starz, H., Stolz, W.,
  ISSN 00390526, 14679884.                                        Vale, E., Weyers, W., Zink, A., Krieghoff-Henning, E.,
                                                                  Kather, J. N., von Kalle, C., Lipka, D. B., Fröhling, S.,
Duchi, J., Khosravi, K., and Ruan, F. Multiclass classifi-        Hauschild, A., Kittler, H., and Brinker, T. J. Skin cancer
  cation, information, divergence and surrogate risk. The         classification via convolutional neural networks: system-
 Annals of Statistics, 46(6B):3246–3275, 2018.                    atic review of studies involving human experts. European
Fan, H., Ferianc, M., Que, Z., Niu, X., Rodrigues, M. L.,        Journal of Cancer, 156:202–216, 2021. ISSN 0959-8049.
  and Luk, W. Accelerating bayesian neural networks via           doi: https://doi.org/10.1016/j.ejca.2021.06.049.
  algorithmic and hardware optimizations. IEEE Transac-         He, K., Zhang, X., Ren, S., and Sun, J. Identity mappings in
  tions on Parallel and Distributed Systems, 2022.                deep residual networks. In Computer Vision–ECCV 2016:
Garcia-Garcia, D. and Williamson, R. C. Divergences and           14th European Conference, Amsterdam, The Netherlands,
  risks for multiclass experiments. In Conference on Learn-       October 11–14, 2016, Proceedings, Part IV 14, pp. 630–
 ing Theory, pp. 28–1. JMLR Workshop and Conference               645. Springer, 2016.
  Proceedings, 2012.                                            Huszar, F. Scoring rules, divergences and information in
                                                                 Bayesian machine learning. PhD thesis, University of
Gilad-Bachrach, R., Navot, A., and Tishby, N. An infor-
                                                                  Cambridge, 2013.
  mation theoretic tradeoff between complexity and accu-
  racy. In Learning Theory and Kernel Machines: 16th            Islam, A., Chen, C.-F., Panda, R., Karlinsky, L., Radke,
  Annual Conference on Learning Theory and 7th Kernel              R. J., and Feris, R. S. A broad study on the transfer-
 Workshop, COLT/Kernel 2003, Washington, DC, USA,                  ability of visual representations with contrastive learning.
  August 24-27, 2003. Proceedings, pp. 595–609. Springer,          2021 IEEE/CVF International Conference on Computer
  2003.                                                           Vision (ICCV), pp. 8825–8835, 2021.
Gneiting, T. and Raftery, A. E. Weather forecasting with        Janowczyk, A. and Madabhushi, A. Deep learning for digital
  ensemble methods. Science, 310:248 – 249, 2005.                 pathology image analysis: A comprehensive tutorial with
                               Popordanoska, Gruber, Tiulpin, Buettner, Blaschko


  selected use cases. Journal of Pathology Informatics, 7:      Murphy, A. H. A new vector partition of the probability
  29, 07 2016. doi: 10.4103/2153-3539.186902.                    score. Journal of Applied Meteorology and Climatology,
                                                                 12(4):595 – 600, 1973. doi: 10.1175/1520-0450(1973)
Joo, T., Chung, U., and Seo, M. Being bayesian about
                                                                 012<0595:ANVPOT>2.0.CO;2.
  categorical probability. In ICML, 2020.
                                                                Murphy, A. H. and Winkler, R. L. Reliability of subjective
Kashinath, K., Mustafa, M., Albert, A., Wu, J., Jiang, C.,
                                                                 probability forecasts of precipitation and temperature.
  Esmaeilzadeh, S., Azizzadenesheli, K., Wang, R., Chat-
                                                                 Journal of the Royal Statistical Society. Series C (Applied
  topadhyay, A., Singh, A., et al. Physics-informed machine
                                                                 Statistics), 26(1):41–47, 1977. ISSN 00359254, 14679876.
  learning: case studies for weather and climate modelling.
  Philosophical Transactions of the Royal Society A, 379        Naeini, M. P., Cooper, G. F., and Hauskrecht, M. Obtaining
 (2194):20200093, 2021.                                           well calibrated probabilities using Bayesian binning. In
                                                                  Proceedings of the Twenty-Ninth AAAI Conference on
Katsaouni, N., Tashkandi, A., Wiese, L., and Schulz, M. H.
                                                                  Artificial Intelligence, pp. 2901–2907, 2015.
  Machine learning based disease prediction from genotype
  data. Biological Chemistry, 402(8):871–885, 2021. doi:        Nguyen, K. and O’Connor, B. Posterior calibration and
  doi:10.1515/hsz-2021-0109.                                      exploratory analysis for natural language processing mod-
                                                                  els. In Proceedings of the 2015 Conference on Empirical
Kristiadi, A., Hein, M., and Hennig, P. Being bayesian,           Methods in Natural Language Processing, pp. 1587–1598,
  even just a bit, fixes overconfidence in relu networks. In      2015.
  ICML, 2020.
                                                                Nixon, J., Dusenberry, M. W., Zhang, L., Jerfel, G., and
Krizhevsky, A. and Hinton, G. Learning multiple layers of         Tran, D. Measuring calibration in deep learning. In
  features from tiny images. Technical Report 0, University       CVPR Workshops, volume 2, 2019.
  of Toronto, Toronto, Ontario, 2009.
                                                                Nobel, A. Histogram regression estimation using data-
Kuleshov, V. and Deshpande, S. Calibrated and sharp               dependent partitions. The Annals of Statistics, 24(3):
  uncertainties in deep learning via density estimation.          1084–1105, 1996.
  In International Conference on Machine Learning, pp.
 11683–11693. PMLR, 2022.                                       Ouimet, F. and Tolosana-Delgado, R. Asymptotic prop-
                                                                  erties of Dirichlet kernel density estimators. Journal of
Kull, M. and Flach, P. Novel decompositions of proper scor-      Multivariate Analysis, 187:104832, 2022.
  ing rules for classification: Score adjustment as precursor
  to calibration. In Machine Learning and Knowledge             Ovcharov, E. Y. Existence and uniqueness of proper scoring
 Discovery in Databases: European Conference, ECML                rules. J. Mach. Learn. Res., 16:2207–2230, 2015.
 PKDD 2015, Porto, Portugal, September 7-11, 2015,              Ovcharov, E. Y. Proper scoring rules and Bregman di-
 Proceedings, Part I 15, pp. 68–85. Springer, 2015.               vergence. Bernoulli, 24(1):53 – 79, 2018. doi: 10.3150/
Kull, M., Perello Nieto, M., Kängsepp, M., Silva Filho, T.,      16-BEJ857.
  Song, H., and Flach, P. Beyond temperature scaling:           Paszke, A., Gross, S., Chintala, S., Chanan, G., Yang, E.,
  Obtaining well-calibrated multi-class probabilities with        DeVito, Z., Lin, Z., Desmaison, A., Antiga, L., and Lerer,
  Dirichlet calibration. Advances in neural information           A. Automatic differentiation in pytorch. In NIPS 2017
  processing systems, 32, 2019.                                  Workshop on Autodiff, 2017.
Kumar, A., Sarawagi, S., and Jain, U. Trainable calibration     Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J.,
  measures for neural networks from kernel mean embed-            Chanan, G., Killeen, T., Lin, Z., Gimelshein, N., Antiga,
  dings. In Dy, J. and Krause, A. (eds.), Proceedings of          L., Desmaison, A., Kopf, A., Yang, E., DeVito, Z., Raison,
 the 35th International Conference on Machine Learning,           M., Tejani, A., Chilamkurthy, S., Steiner, B., Fang, L.,
  volume 80 of Proceedings of Machine Learning Research,          Bai, J., and Chintala, S. Pytorch: An imperative style,
  pp. 2805–2814. PMLR, 10–15 Jul 2018.                            high-performance deep learning library. In Wallach, H.,
Kumar, A., Liang, P., and Ma, T. Verified uncertainty             Larochelle, H., Beygelzimer, A., d'Alché-Buc, F., Fox, E.,
  calibration. In Proceedings of the 33rd International           and Garnett, R. (eds.), Advances in Neural Information
 Conference on Neural Information Processing Systems,             Processing Systems 32, 2019.
  pp. 3792–3803, 2019.                                          Platt, J. C. Probabilistic outputs for support vector ma-
Liese, F. and Vajda, I. On divergences and informations in        chines and comparisons to regularized likelihood methods.
  statistics and information theory. IEEE Transactions on         In Advances in Large-Margin Classifiers, pp. 61–74. MIT
  Information Theory, 52(10):4394–4412, 2006.                     Press, 1999.
                                                                Popordanoska, T., Sayer, R., and Blaschko, M. B. A con-
MacKay, D. J. Information theory, inference and learning
                                                                  sistent and differentiable lp canonical calibration error
 algorithms. Cambridge university press, 2003.
                                                                  estimator. In Oh, A. H., Agarwal, A., Belgrave, D., and
Menon, A. K., Rawat, A. S., Reddi, S. J., Kim, S., and            Cho, K. (eds.), Advances in Neural Information Process-
 Kumar, S. A statistical perspective on distillation. In          ing Systems, 2022.
 ICML, 2021.
                                                                Rahimi, A., Shaban, A., Cheng, C.-A., Hartley, R., and
Minderer, M., Djolonga, J., Romijnders, R., Hubis, F.,            Boots, B. Intra order-preserving functions for calibra-
  Zhai, X., Houlsby, N., Tran, D., and Lucic, M. Revisiting       tion of multi-class neural networks. Advances in Neural
  the calibration of modern neural networks. Advances in          Information Processing Systems, 33:13456–13467, 2020.
 Neural Information Processing Systems, 34, 2021.
                                                                Roelofs, R., Cain, N., Shlens, J., and Mozer, M. C. Mitigat-
Morales-Álvarez, P., Hernández-Lobato, D., Molina, R., and        ing bias in calibration error estimation. In International
 Hernández-Lobato, J. M. Activation-level uncertainty in         Conference on Artificial Intelligence and Statistics, pp.
 deep neural networks. In ICLR, 2021.                             4036–4054. PMLR, 2022.
             Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors


Saxe, A. M., Bansal, Y., Dapello, J., Advani, M., Kolchinsky,    Zaremba, W., Gretton, A., and Blaschko, M. B-tests: Low
  A., Tracey, B. D., and Cox, D. D. On the information             variance kernel two-sample tests. In Burges, C., Bot-
  bottleneck theory of deep learning. In International             tou, L., Welling, M., Ghahramani, Z., and Weinberger,
  Conference on Learning Representations, 2018.                    K. (eds.), Advances in Neural Information Processing
Shamir, O., Sabato, S., and Tishby, N. Learning and gen-           Systems, volume 26, 2013.
  eralization with the information bottleneck. Theoretical       Zhang, J., Kailkhura, B., and Han, T. Y.-J. Mix-n-match:
  Computer Science, 411(29-30):2696–2711, 2010.                    Ensemble and compositional methods for uncertainty
Shwartz-Ziv, R. and Tishby, N. Opening the black box of            calibration in deep learning. In International Conference
  deep neural networks via information. arXiv preprint             on Machine Learning, pp. 11117–11128. PMLR, 2020.
  arXiv:1703.00810, 2017.
Simonyan, K. and Zisserman, A. Very deep convolutional
  networks for large-scale image recognition. arXiv preprint
  arXiv:1409.1556, 2014.
Slonim, N. and Tishby, N. Agglomerative information
  bottleneck. Advances in neural information processing
  systems, 12, 1999.
Tian, J., Yung, D., Hsu, Y.-C., and Kira, Z. A geomet-
  ric perspective towards neural calibration via sensitivity
  decomposition. In NeurIPS, 2021.
Tomani, C., Gruber, S., Erdem, M. E., Cremers, D., and
  Buettner, F. Post-hoc uncertainty calibration for do-
  main drift scenarios. In Proceedings of the IEEE/CVF
  Conference on Computer Vision and Pattern Recognition
  (CVPR), pp. 10124–10132, June 2021.
Vaicenavicius, J., Widmann, D., Andersson, C., Lindsten,
  F., Roll, J., and Schön, T. Evaluating model calibration
  in classification. In The 22nd International Conference
  on Artificial Intelligence and Statistics, pp. 3459–3467.
  PMLR, 2019.
Wang, X., Liu, H., Shi, C., and Yang, C. Be confident!
  towards trustworthy graph neural networks via confidence
  calibration. In NeurIPS, 2021.
Wang, Z., Huang, S.-L., Kuruoglu, E. E., Sun, J., Chen,
  X., and Zheng, Y. PAC-bayes information bottleneck. In
  International Conference on Learning Representations,
  2022.
Wenger, J., Kjellström, H., and Triebel, R. Non-parametric
  calibration for classification. In International Confer-
  ence on Artificial Intelligence and Statistics, pp. 178–190,
  2020.
Widmann, D., Lindsten, F., and Zachariah, D. Calibration
  tests in multi-class classification: A unifying framework.
  Advances in Neural Information Processing Systems, 32:
  12257–12267, 2019.
Williamson, R. C. The geometry of losses. In Conference
  on Learning Theory, pp. 1078–1108. PMLR, 2014.
Wolter, K. M. Introduction to Variance Estimation.
  Springer, 2007.
Wu, T. and Fischer, I. Phase transitions for the information
  bottleneck in representation learning. In International
  Conference on Learning Representations, 2020.
Wu, T., Fischer, I., Chuang, I. L., and Tegmark, M. Learn-
  ability for the information bottleneck. In Uncertainty in
  Artificial Intelligence, pp. 1050–1060. PMLR, 2020.
Yurtsever, E., Lambert, J., Carballo, A., and Takeda, K.
  A survey of autonomous driving: Common practices
  and emerging technologies. IEEE access, 8:58443–58469,
  2020.
Zagoruyko, S. and Komodakis, N. Wide residual networks.
  In British Machine Vision Conference 2016. British Ma-
  chine Vision Association, 2016.
                             Popordanoska, Gruber, Tiulpin, Buettner, Blaschko


A    Uncertainty calibration in classification

In this section, we give a more detailed overview of calibration errors compared
                                                                              n      to the main paper. To introduce
                                                                                                                 o
                                                                                          ⊺        k Pk
calibration formally, we consider a classifier g : X → ∆k , where ∆k := (p1 , . . . , pk ) ∈ [0, 1] | i=1 pi = 1 is
a probability simplex with k vertices, and X is a feature space with feature variable X. We denote class labels
as one-hot encoded variables of Y = {1, . . . , k}, i.e. the target variable Y has observations y ∈ {0, 1}k ⊂ ∆k with
∥y∥1 = 1. In the literature, there exist multiple notions of calibration of different strength (Vaicenavicius et al.,
2019; Kull et al., 2019). Calibration errors assess the degree of violation of a respective notion.
The strongest notion of calibration is the canonical calibration, which compares the probability vector prediction
g (X) with the target distribution E [Y | g (X)] given this prediction. A class of canonical calibration errors, which
was studied recently in several works (Naeini et al., 2015; Kumar et al., 2019; Wenger et al., 2020; Popordanoska
et al., 2022; Gruber & Buettner, 2022), is referred to as Lp calibration error and defined as

                                               h                       i p1
                                                                      p
                                    CEp (f ) = E ∥E [Y | g(X)] − g(X)∥p       .                                  (23)

                 d2 , as given in Equation (5), can be derived from the Brier score (Murphy, 1973).
The special case CE2

Canonical calibration errors are notoriously difficult to estimate and represent a calibration strictness which may
not be necessary in practice (Vaicenavicius et al., 2019). One common and less constraining notion is class-wise
calibration, which compares the individual prediction gi (X) of class i ∈ Y with the target class distribution
P (Y = i | gi (X)) given the individual class prediction. The class-wise calibration error with respect to a given
Lp space is defined as

                                                k
                                                                                     ! p1
                                             1X                                    p
                            CWCEp (g) =            E [(P (Y = i | gi (X)) − gi (X)) ]     .                      (24)
                                             k i=1

The definition is formalized based on Kumar et al. (2019) and Gruber & Buettner (2022), while the class-wise
concept was introduced independently by Kull et al. (2019) and Nixon et al. (2019).
While class-wise calibration is easier to evaluate than canonical calibration, it still scales linearly in complexity
with the number of classes, which can be problematic for tasks with a very high number of classes. In contrast, the
most common approach in the machine learning literature is top-label confidence calibration (Naeini et al., 2015;
Guo et al., 2017; Joo et al., 2020; Kristiadi et al., 2020; Rahimi et al., 2020; Tomani et al., 2021; Minderer et al.,
2021; Tian et al., 2021; Islam et al., 2021; Menon et al., 2021; Morales-Álvarez et al., 2021; Gupta et al., 2021;
Wang et al., 2021; Fan et al., 2022), which is not affected by this issue. In this notion, we compare if the predicted
top-label confidence maxi∈Y gi (X) matches the conditional accuracy P (Y = arg maxi∈Y gi (X) | maxi∈Y gi (X))
given the predicted top-label confidence. It is known in the literature that top-label confidence calibration
represents the weakest notion of calibration (Vaicenavicius et al., 2019; Widmann et al., 2019; Gruber & Buettner,
2022). The top-label confidence calibration error based on an Lp space is defined as (Kumar et al., 2019; Gruber
& Buettner, 2022)


                                                                           p  p1
                 TCEp (g) =    E P Y = arg max gj (X) | max gj (X) − max gj (X)          .                       (25)
                                                  j∈Y           j∈Y             j∈Y


For p = 1, its binning based estimator is commonly referred to as expected calibration error (Naeini et al., 2015;
Guo et al., 2017).
Besides the Lp based calibration errors presented above, there also exist other calibration errors, like maximum
mean calibration error (Kumar et al., 2018), Kolmogorov-Smirnov calibration error (Gupta et al., 2020), and
kernel calibration error (Widmann et al., 2019). We exclude these errors from our analysis and experiments as
they are not related to risk minimization.
            Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors


B     Proofs for information monotonicity

In this section, we provide detailed proofs about the f-divergence representation of the model sharpness and the
information monotonicity in neural networks. Since we will require the target variable Y in categorical encoding
and one-hot encoding, we will write Y for the former and Y    ⃗ for the latter. This notation is exclusive to this
section.


B.1   Proof of Proposition 6.1

Let F : ∆k → R be a convex function and g : X → ∆k a classifier with prediction distributions Py :=
P (g (X) | Y = y), and P := P (g (X)). Then, the model sharpness can be represented as an f-divergence
via

                SHARPF (g)
                      h    h           i h ii
                = E DF E Y    ⃗ | g (X) , E Y  ⃗
                      h  h           i         h i D         h i h i         h          iEi
                def         ⃗ | g (X) − F E Y       ⃗              ⃗ ,E Y    ⃗ −E Y  ⃗ | g (X)
                = E F E Y                                 − ∇F E Y
                      h  h           ii         h i
                =E F E Y    ⃗ | g (X)      −F E Y    ⃗
                    Z     h           i        h i
                =       F E Y⃗ | g (X) − F E Y       ⃗ dP (g (X))
                     X                                                                                           (26)
                          h i                               h i dP (g (X) | Y = k) 
                                  dP (g (X) | Y = 1)
                    Z
                =            ⃗
                        F E Y1                                ⃗k
                                                       ,...,E Y
                     X                dP (g (X))                     dP (g (X))
                           h i
                             ⃗
                      − F E Y dP (g (X))
                    Z     h i                 h i dP 
                             ⃗1 dP1 , . . . , E Y
                                                               h i
                                                 ⃗k     k         ⃗ dP
                =       F E Y                              −F E Y
                     X            dP                 dP
                 = IF Y (P1 , . . . , Pk ∥ P )

                   h i                h i        h i            h i
                     ⃗ 1 x1 , . . . , E Y
where F Y (x) := F E Y                  ⃗ k xk − F E Y
                                                     ⃗1 , . . . , E Y
                                                                    ⃗k  and by using Bayes’ theorem. The
                                                              Y
function IF Y is a multi-distribution
                      h i                      h i since Fh i
                                     h if-divergence           is convex (follows from F being convex) and
  Y                    ⃗              ⃗            ⃗          ⃗
F (1, . . . , 1) = F E Y1 , . . . , E Yk − F E Y1 , . . . , E Yk = 0.


B.2   Proof of Theorem 6.2

For a neural network g (X) = hl (. . . (h1 (X))) with layers hi , i ∈ {1, . . . , l}, conditional distributions Pyi :=
                                                                     
P (hi (. . . (h1 (X))) | Y = y), and marginal distributions P i := E PYi , we have

                       SHARPF (g) = IF Y P1l , . . . , Pkl ∥ P l ≤ IF Y P1l−1 , . . . , Pkl−1 ∥ P l−1
                                                                                                     
                                                                                                                 (27)
                                  ≤ · · · ≤ IF Y P11 , . . . , Pk1 ∥ P 1 ≤ SIF (X; Y ) .
                                                                        




Proof. Since a neural network in our context is simply a chain of function, it is sufficient to prove that the
inequality holds for a single arbitrary function f transforming a sample space Ω with σ-field F . For this, assume
we are in the context of a probability space (Ω, F , P) and measurable space (Ωf , Ff ) such that f : Ω → Ωf is
a measurable function. Define the function Mf : Ω × Ff → R via Mf (ω, A) = 1{ω∈Ω|f (ω)∈A}     R (ω), where 1 is
the indicator function. Similar as Garcia-Garcia & Williamson (2012), we write Mf P (A) = Ω Mf (ω, A) dP (ω).
Now, we simply have to show that Mf is a Markov kernel, which then proves the statement via the information
monotonicity of f-divergences.
                              Popordanoska, Gruber, Tiulpin, Buettner, Blaschko


For A ∈ Ff we have
                                                     Z
                                       Mf P (A) =         Mf (ω, A) dP (ω)
                                                     ZΩ
                                                 =        1{ω∈Ω|f (ω)∈A} (ω) dP (ω)
                                                     Ω
                                                     Z                                                           (28)
                                                 =                   dP
                                                     {ω∈Ω|f (ω)∈A}

                                                 = P ({ω ∈ Ω | f (ω) ∈ A}) .

The last line shows that Mf P maps into a distribution space, which fulfills the definition of a Markov kernel as
given in (Garcia-Garcia & Williamson, 2012).
Now, using the information monotonicity of f-divergences, we get for i ∈ {2, . . . , l}

                       IF Y P1i , . . . , Pki ∥ P i = IF Y Mgi P1i−1 , . . . , Mgi Pki−1 ∥ Mgi P i−1
                                                                                                    
                                                                                                             (29)
                                                     ≤ IF Y P1i−1 , . . . , Pki−1 ∥ P i−1 ,
                                                                                         

which proves the inequality chain. It is upper bounded by the statistical information since

              IF Y P11 , . . . , Pk1 ∥ P 1
                                           

                = IF Y (Mg1 P (X | Y = 1) , . . . , Mg1 P (X | Y = k) ∥ Mg1 P (X))
                ≤ IF Y (P (X | Y = 1) , . . . , P (X | Y = k) ∥ P (X))
                          h i                              h i dP (X | Y = k) 
                              ⃗1 dP (X | Y = 1) , . . . , E Y
                  Z                                                                 h i
                =      F E Y                                 ⃗k                       ⃗ dP (X)
                                                                                 −F E Y                          (30)
                   X                 dP (X)                          dP (X)
                    h  h         ii           h i
                =E F E Y    ⃗ |X      −F E Y        ⃗

                = SIF (X; Y ) .



C    Class-wise calibration induced by One-vs-Rest risk

In this section, we derive class-wise calibration errors from One-vs-Rest risk minimization. We do so by decomposing
the One-vs-Rest risk into calibration and sharpness terms analogous to the standard risk minimization case. This
is a novel contribution towards better understanding of class-wise calibration errors. Specifically, this suggests to
use class-wise calibration in predictive scenarios when the multi-class prediction consists of probabilities, which
do not sum up to one.
For a binary loss L : [0, 1] × {0, 1} → R, we define the risk of class i vs the rest as


                                          Ri (g) := E [L (g (X) , 1 {Y = i})] ,                                  (31)

where g : X → [0, 1] is a binary classifier and Y takes values in {1, . . . , k}.
In the following, we assume −L is a proper score, i.e. it is minimized by the Bayes classifier.
Analogous, the negative Bayes risk for a q ∈ [0, 1] is given by


                                           F (q) := − inf EY ∼q [L (p, Y )] .                                    (32)
                                                         p∈[0,1]


Like in the canonical case, F is convex as long as −L is a proper score. Consequently, DF is a Bregman divergence.
                                                                                               2
The Brier score and the squared Euclidean distance are recovered by F (q) = q 2 + (1 − q) . The negative log
likelihood and the Kullback–Leibler divergence are given by the case F (q) = q log q + (1 − q) log (1 − q). As a
novel contribution, we derive class-wise calibration errors from the mean of the class-wise One-vs-Rest risk of
binary classifiers g1 , . . . , gk as
             Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors


                  k                k
               1X               1X
                     Ri (gi ) =       −F (P (Y = i)) + CWCEF (g1 , . . . , gk ) − SHARPF (g1 , . . . , gk )               (33)
               k i=1            k i=1
                                                                           Pk
where we have a class-wise calibration error CWCEF (g1 , . . . , gk ) := k1 i=1 E [DF (P (Y = i | gi (X)) , gi (X))]
                                                          Pk
and a class-wise sharpness SHARPF (g1 , . . . , gk ) := k1 i=1 E [DF (P (Y = i | gi (X) , P (Y = i)))]. Analogous to
                                                                                                                        ⊺
the canonical case, we have CWCEF (g1 , . . . , gk ) = CWCE22 (g) for F (q) = q 2 and g (x) := (g1 (x) , . . . , gk (x)) .
Surprisingly, the associated negative Bayes risk is not symmetric unlike other common cases (Gneiting & Raftery,
2007). Note that the factor k1 systematically decreases the class-wise calibration error with growing k if the
class-wise predictions are normalized to a probability vector (Gruber & Buettner, 2022).

Proof. We first show that the decomposition holds. Note that we implied F is differentiable, but the decomposition
still holds under general conditions by replacing Bregman divergences with score divergences (Gneiting & Raftery,
2007). Since by assumption L is a negative proper score, we have L (p, y) = −F (p) − F ′ (p) (y − p) for p ∈ [0, 1]
and y ∈ {0, 1} (c.f. Schervish representation (Gneiting & Raftery, 2007)).
Further, note that for i ∈ {1, . . . , k} we have
                    Ri (gi )
                     = E [L (gi (X) , 1 {Y = i})]
                     def

                     = E [−F (gi (X)) − F ′ (gi (X)) (1 {Y = i} − gi (X))]
                  LOTUS
                     =     E [−F (gi (X)) − F ′ (gi (X)) (P (Y = i | gi (X)) − gi (X))]                                   (34)
                     = E [DF (P (Y = i | gi (X)) , gi (X))] − E [F (E (Y = i | gi (X)))]
                     = E [DF (P (Y = i | gi (X)) , gi (X))] − E [DF (P (Y = i | gi (X)) , P (Y = i))]
                           − E [F (P (Y = i | gi (X)))] ,

where we used the law of the unconscious statistician (LOTUS) and the definition of Bregman divergences.
Now, we use this result to get


                  k                k
               1X               1X
                     Ri (gi ) =       −F (P (Y = i))
               k i=1            k i=1
                                              k
                                           1X
                                       +         E [DF (P (Y = i | gi (X)) , gi (X))]
                                           k i=1
                                                                                                                          (35)
                                              k
                                         1X
                                       −       E [DF (P (Y = i | gi (X)) , P (Y = i))]
                                         k i=1
                                       k
                               def 1
                                       X
                               =            −F (P (Y = i)) + CWCEF (g1 , . . . , gk ) − SHARPF (g1 , . . . , gk ) .
                                   k i=1

                                                                                                                      ⊺
Last, we show CWCEF (g1 , . . . , gk ) = CWCE22 (g) for F (q) = q 2 and g (x) := (g1 (x) , . . . , gk (x)) . Since
                   2
DF (x, y) = (x − y) , we have


                                                               k
                                                       def 1
                                                               X
                           CWCEF (g1 , . . . , gk ) =                E [DF (P (Y = i | gi (X)) , gi (X))]
                                                             k i=1
                                                                k
                                                             1X h                                  2
                                                                                                     i                    (36)
                                                       =           E (P (Y = i | gi (X)) − gi (X))
                                                             k i=1
                                                       def
                                                       = CWCE22 (g) .
                                   Popordanoska, Gruber, Tiulpin, Buettner, Blaschko


D        Proper calibration error estimators via KDE

D.1       The Dirichlet kernel in estimating E[Y | g(x)]

The Dirichlet kernel is defined as:
                                                                  PK         K
                                                                Γ( k=1 αjk ) Y        α −1
                                        kDir (g(xh ), g(xj )) = QK              g(xh )k jk                                               (37)
                                                                  k=1 Γ(α  )
                                                                         jk k=1


              g(x )
with αj = γ j + 1, γ > 0 being a bandwidth parameter (Ouimet & Tolosana-Delgado, 2022; Popordanoska et al.,
2022). We note that popular libraries such as PyTorch provide only log Γ2 and not Γ directly (Paszke et al.,
2019). It will therefore be useful to consider
                                           PK          K
                                         Γ(      αjk ) Y        α −1
            log(k(g(xh ), g(xj ))) = log QK k=1           g(xh )k jk                                                                     (38)
                                           k=1 Γ(α   )
                                                   jk k=1
                                             K
                                                    !    K                K
                                            X          X                  X
                                   = log Γ      αjk −      log Γ (αjk ) +   (αjk − 1) log g(xh )k                                        (39)
                                              k=1              k=1                         k=1
                                                    K
                                                                     !       K                           
                                                    X     g(xj )k            X                 g(xj )k      1
                                   = log Γ K +                           −         log Γ               + 1 + ⟨g(xj ), log(g(xh ))⟩       (40)
                                                            γ                                    γ          γ
                                                    k=1                      k=1


and we can further apply the log to the softmax function in the last log(g(xh )) inside the inner product.
We subsequently focus on terms of the form
                                                         
                                   X
                          log          k(g(xh ), g(xj )) = LogSumExpj̸=h (log(k(g(xh ), g(xj )))) .                                    (41)
                                 j̸=h

                                     P                              
Computation of terms of the form log     j̸=h k(g(x h ), g(x j ))y j   are essentially the same, but the LogSumExp
operation should only be performed over indices where yjk ̸= 0.

D.2       Bregman derivation of the L2 calibration error estimator

For the Bregman formulation of squared L2 error, we have F (x) = ∥x∥22 , and the r.h.s. of Equation (7) becomes

                      n   P                               2                          *            P                             +!
                1X            j̸=h k(g(xh ), g(xj ))yj                                               j̸=h k(g(xh ), g(xj ))yj
                           P                                  + ∥g(xh )∥22 − 2           g(xh ), P
                n              j̸=h k(g(xh ), g(xj ))                                                 j̸=h k(g(xh ), g(xj ))
                  h=1                                     2
                                                                               n      P                                          2
                                                                       1X                  j̸=h k(g(xh ), g(xj ))yj
                                                                     =                   P                            − g(xh )       .   (42)
                                                                       n                    j̸=h k(g(xh ), g(xj ))
                                                                              h=1                                                2


We see that this recovers exactly the L2 special case of the estimator given by (Popordanoska et al., 2022,
Equation(9)). That paper shows that the resulting estimator is consistent, and has a convergence of O(n−1/2 )
with a bias that converges as O(n−1 ).

D.3       Bregman derivation of the KL calibration error estimator

Recall from above that the Bregman KL divergence is generated by F (p) = ⟨p, log(p)⟩, where the log operation is
applied element-wise.
    2
        https://pytorch.org/docs/stable/generated/torch.lgamma.html
             Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors


The Bregman formulation of KL calibration error is
            n
                *P                                      P                            !+
         1X          j̸=h k(g(xh ), g(xj ))yj             j̸=h k(g(xh ), g(xj ))yj
                   P                            , log    P                                 − ⟨g(xh ), log(g(xh ))⟩−
         n
           h=1         j̸=h k(g(xh ), g(xj ))               j̸=h k(g(xh ), g(xj ))
                                                     *                   P                                     +!
                                                                            j̸=h k(g(xh ), g(xj ))yj
                                                       log(g(xh )) + e, P                              − g(xh )
                                                                              j̸=h k(g(xh ), g(xj ))
                                    n
                                        *P                                        P                             !+
                                1X            j̸=h k(g(xh ), g(xj ))yj                j̸=h k(g(xh ), g(xj ))yj
                              =             P                          , log P                                               (43)
                                n               j̸=h k(g(xh ), g(xj ))             j̸=h k(g(xh ), g(xj ))g(xh )
                                       h=1

where e is a vector of all ones and division of two vectors is assumed to be element-wise. The result is an estimator
identical to Equation (8).

D.4     General Sharpness-Calibration error decompositions of expectations of Bregman divergences

In general, we can define a statistical risk measure based on a Bregman divergence as

                   E(X,Y )∼p [DF (Y, g(X))] = E(X,Y ) [F (Y ) − F (g(X)) − ⟨∇F (g(X)), Y − g(X)⟩].                           (44)

If we subtract out the associated Bregman calibration error (cf. Equation (7)), we have

        E[DF (Y, g(X))] − CEF (g) =E(X,Y ) [DF (Y, g(X))] − EX [DF (E[Y | g(X)], g(X))]                                      (45)
                                       =E[F (Y ) − F (g(X)) − ⟨∇F (g(X)), Y − g(X)⟩]                                         (46)
                                         − E[F (E[Y | g(X)]) − F (g(X)) − ⟨∇F (g(X)), E[Y | g(X)] − g(X)⟩]
                                       =E[F (Y ) − F (E[Y | g(X)])] − E[⟨∇F (g(X)), Y − E[Y | g(X)]⟩].                       (47)

It is a well known property of conditional expectation that E[f (Z) · Y | Z] = f (Z)E[Y | Z], which yields

      E[⟨∇F (g(X)), Y − E[Y | g(X)]⟩] =E[⟨∇F (g(X)), Y ⟩] −                E[E[⟨∇F (g(X)), Y ⟩ | g(X)]]               = 0,   (48)
                                                                           |          {z             }
                                                                     =E[⟨∇F (g(X)),Y ⟩] by law of total expectation


and our equation simplifies to

                               E[DF (Y, g(X))] − CEF (g) = E[F (Y ) − F (E[Y | g(X)])].                                      (49)

D.4.1     Recovery of L2 refinement

Setting F (p) = ∥p∥2 , the risk becomes the Brier score and we obtain

                                  E[∥Y ∥2 − ∥E[Y | g(X)]∥2 ] =1 − EX [∥E[Y | g(X)]∥2 ]                                       (50)

Popordanoska et al. (2022) show the L2 refinement to be E[(1 − E[Y | g(X))]E[Y | g(X)]] = E[E[Y | g(X)] − E[Y |
g(X)]2 ] = E[Y ] − E[E[Y | g(X)]2 ]. This is in fact the first term of the above if we expand the norm as a sum over
elements and split into expectations of terms from each dimension of Y .

D.4.2     Recovery of KL refinement

Setting F (p) = ⟨p, log(p)⟩, the risk corresponds with cross-entropy loss, and we obtain

                E[⟨Y, log(Y )⟩ −⟨E[Y | g(X)], log(E[Y | g(X)]⟩] = − E[⟨E[Y | g(X)], log(E[Y | g(X)]⟩]                        (51)
                  | {z }
                       =0
                                                                    =E[H(E[Y | g(X)])],                                      (52)

where H denotes entropy, we interpret the first inner product involving Y using limY ↘0 Y log Y = 0 as it is
otherwise undefined, and we additionally assume categorical labels Y without uncertainty.
                                                      Popordanoska, Gruber, Tiulpin, Buettner, Blaschko


E              Experiments

In this section, we first provide a detailed description of the empirical setup. Subsequently, we further investigate
the bias convergence of our estimator, both on simulated and real-world datasets. Then, we show a table
evaluating accuracy, NLL and Brier score on CIFAR 10/100 before and after calibration with isotonic regression
and temperature scaling. Finally, we present additional results for several use-cases of the estimator: monitoring
model training, model selection, and assessing calibration error.

E.1            Empirical setup

Datasets The experiments in the main text rely on two widely used benchmark datasets, CIFAR-10/100
(Krizhevsky & Hinton, 2009), which consist of 32 × 32 natural images divided into 10 and 100 classes, respectively.
We split the data into train/validation/test sets of 45000/5000/10000.

Models We trained PreResNet20, PreResNet56, PreResNet110, PreResNet164 (He et al., 2016), VGG16 (with
BatchNorm) (Simonyan & Zisserman, 2014) and WideResNet28x10 (Zagoruyko & Komodakis, 2016) for 250
epochs with Stochastic Gradient Descent optimizer using PyTorch (Paszke et al., 2017). The learning rate was
reduced by a factor of 10 at 150th and 225th epochs. The WideResNet and the PreResNet models were trained
with the learning rate of 1e−1, batch size of 128, weighted decay (WD) of 1e−10 and Nesterov’s momentum of
0.9. During the first epoch, we warmed up the training with the learning rate of 0.01. The VGG model was
trained with the learning rate of 5e−2, WD of 5e−5, batch size of 128, and momentum of 0.05. The training was
carried out with NVIDIA V100 GPU.

E.2            Convergence of bias

In addition to our empirical analysis for the convergence of bias on simulated data in the main part, here we
present the calibration error and the relative bias, computed as CE−CE  ∗ 100, with c
                                                                                    CE the estimated and CE
                                                                  c
                                                                   CE
the ground truth calibration error. The averaged results across 20 iterations of sampling new points for the
estimation, together with the standard errors, are shown in Figure 3.

        0.10                                                  0.10                                                0.10                                                                   250
                                     Ground truth                                         Ground truth                                        Ground truth                                                            2 classes
                                     CE22                                                 CE22                                                CE22                                                                    5 classes
                                                                                                                                                                                         200                          10 classes




                                                                                                                                                               Relative CE22 bias (%)
        0.08                                                  0.08                                                0.08

                                                                                                                                                                                         150
        0.06                                                  0.06                                                0.06
 CE22                                                  CE22                                                CE22
                                                                                                                                                                                         100
        0.04                                                  0.04                                                0.04

                                                                                                                                                                                          50
        0.02                                                  0.02                                                0.02
                                                                                                                                                                                           0
                0       5000       10000      15000                  0       5000       10000      15000                 0       5000       10000      15000                                   0   5000       10000          15000
                        Number of points                                     Number of points                                    Number of points                                                  Number of points


                    (a) 2 classes                                        (b) 5 classes                                       (c) 10 classes                                               (d) Relative CE
                                                                                                                                                                                                       d2 bias
                                                                                                                                                                                                         2
        0.25                                                  0.25                                                0.25                                                                   250
                                     Ground truth                                         Ground truth                                        Ground truth                                                            2 classes
                                     CEKL                                                 CEKL                                                CEKL                                                                    5 classes




                                                                                                                                                                Relative CEKL bias (%)
                                                                                                                                                                                         200                          10 classes
        0.20                                                  0.20                                                0.20

                                                                                                                                                                                         150
 CEKL   0.15                                           CEKL   0.15                                         CEKL   0.15
                                                                                                                                                                                         100

        0.10                                                  0.10                                                0.10
                                                                                                                                                                                         50


        0.05                                                  0.05                                                0.05                                                                    0
               0        5000       10000      15000                  0       5000       10000      15000                 0       5000       10000      15000                                   0   5000       10000          15000
                        Number of points                                     Number of points                                    Number of points                                                  Number of points


                    (e) 2 classes                                        (f) 5 classes                                       (g) 10 classes                                              (h) Relative c
                                                                                                                                                                                                      CEKL bias

Figure 3: Calibration error and relative bias (%) on simulated data for different number of classes. Each plot
                                                                            d2 , while the bottom row c
shows the estimate as a function of the sample size. The top row evaluates CE                         CEKL .
                                                                               2


Similarly, in Figure 4 we evaluate the calibration error, bias and relative bias on the test set of CIFAR-10, as a
function of the number of points used for the estimation. The ground truth is calculated from the whole test
                   Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors


                                                Ground truth                      0.008
                                                                                                                                                                    40
               0.026                            CEKL




                                                                                                                                          Relative CEKL bias (%)
                                                                                  0.006                                                                             30
               0.024


                                                                     CEKL bias
                                                                                  0.004                                                                             20
        CEKL   0.022
                                                                                  0.002                                                                             10
               0.020
                                                                                  0.000                                                                                 0
               0.018
                                                                                 −0.002                                                                            −10
                       0    2000    4000    6000    8000   10000                           0      2000    4000    6000    8000   10000                                          0   2000     4000    6000    8000   10000
                                   Number of points                                                      Number of points                                                                   Number of points

                                                                                                                                                                   30
                                                 Ground truth
                                                                                 0.002
                                                 CE22




                                                                                                                                         Relative CE22 bias (%)
               0.010
                                                                                                                                                                   20


                                                                     CE22 bias
                                                                                 0.001
        CE22   0.009                                                                                                                                               10


                                                                                 0.000                                                                              0
               0.008


                       0    2000    4000    6000    8000   10000                          0      2000     4000    6000    8000   10000                                      0       2000    4000    6000    8000    10000
                                   Number of points                                                      Number of points                                                                  Number of points


Figure 4: Calibration error, bias, and relative bias (%) evaluated on the test set of CIFAR 10, using predictions of
trained PreResNet56 architectures with four different seeds. The ground truth is obtained from the whole test set.


set (10000 images). The bandwidth of the Dirichlet kernel is set to 0.02. The results reveal that the estimator
achieves values that closely align with the ground truth, even with as few as a (couple of) hundred points.

E.3   Post-hoc calibration
                                                                  d2 and CE
In addition to the experiment in the main text, where we evaluate CE     c KL before and after calibration, in
                                                                    2
Table 4 we show accuracy, NLL and Brier score of various network architectures on CIFAR-10/100.

Table 4: Performance evaluation (Acc ×100, NLL ×100 and Brier score ×100) of various network architectures
on CIFAR-10/100 with no calibration, and recalibration with Isotonic Regression and Temperature Scaling.

                                                           No calibration                                           Isotonic Regression                                                       Temperature Scaling
  Dataset                  Model                 Acc           NLL                            Brier           Acc           NLL        Brier                                               Acc       NLL        Brier
                   PreResNet20               91.95±0.05         32.65±0.45               12.75±0.08        91.94±0.07     26.92±0.09       11.99±0.07                               91.95±0.05        24.11±0.14      11.74±0.07
                   PreResNet56               94.38±0.13         22.46±0.25               9.03±0.18         94.34±0.13     19.58±0.19       8.61±0.14                                94.38±0.13        17.48±0.17      8.41±0.13
                   PreResNet110              94.86±0.04         20.42±0.18               8.24±0.06         94.83±0.05     18.06±0.34       7.91±0.04                                94.86±0.04        16.11±0.07      7.72±0.06
  CIFAR-10
                   PreResNet164              95.24±0.05         18.61±0.29               7.58±0.06         95.14±0.06     17.39±0.33       7.33±0.07                                95.24±0.05        14.96±0.17      7.13±0.06
                     VGG16BN                 93.26±0.04         33.76±0.29               11.61±0.10        93.23±0.04     25.15±0.33       10.42±0.08                               93.26±0.04        24.55±0.16      10.48±0.09
                  WideResNet28x10            95.54±0.05         15.69±0.16               7.00±0.07         95.53±0.04     16.49±0.44       6.86±0.08                                95.54±0.05        14.50±0.17      6.80±0.09
                   PreResNet20               68.01±0.15      121.48±1.12                 44.38±0.15        67.58±0.13     134.53±1.92      44.60±0.07                               68.01±0.15       113.17±0.30      42.95±0.09
                   PreResNet56               74.38±0.10      112.80±2.88                 38.24±0.43        74.00±0.09     115.75±1.44      36.88±0.17                               74.38±0.10        93.10±1.02      35.41±0.21
                   PreResNet110              75.62±0.14      106.74±0.53                 36.44±0.17        75.26±0.09     108.38±1.00      35.25±0.15                               75.62±0.14        88.82±0.45      33.83±0.15
 CIFAR-100
                   PreResNet164              76.54±0.05      103.19±0.55                 35.12±0.13        76.11±0.10     108.24±0.85      34.18±0.12                               76.54±0.05        86.30±0.54      32.68±0.13
                     VGG16BN                 71.36±0.08      167.78±0.98                 46.45±0.16        71.08±0.18     137.77±0.91      40.96±0.14                               71.36±0.08       120.41±0.51      39.77±0.13
                  WideResNet28x10            79.56±0.22       84.17±0.80                 29.93±0.31        79.23±0.21      99.28±1.49      29.92±0.28                               79.56±0.22        81.83±0.68      29.44±0.29



E.4   Additional experiments

Monitoring calibration error during training Monitoring accuracy and loss during the training of a
deep neural network is essential for various reasons, including performance evaluation and model selection. We
argue that monitoring calibration error and sharpness/refinement, in addition to the standard metrics, provides
additional insights into the reliability and performance of the model.
We trained VGG16 (Simonyan & Zisserman, 2014) on a binary classification task, using a publicly available
dataset of breast histopathology images (Janowczyk & Madabhushi, 2016). We used 10% of the image patches
from the dataset, ensuring that the original 70:30 ratio of negative to positive points is maintained. We apply
                                                   Popordanoska, Gruber, Tiulpin, Buettner, Blaschko


a smoothing technique (exponential moving average) to improve clarity. In Figure 5 we show the training and
validation metrics per epoch and we observe several trends. For instance, we notice that as the model overfits
and validation loss increases, the refinement remains fairly flat, and the increase in validation loss is only due to
the increasing calibration error. CE
                                  c KL not only correctly uncovers an early stopping point (same as the loss), but
it also offers a more refined view of the nature of overfitting: while the validation accuracy remains constant, the
CE considerably increases. For these reasons, we advocate for incorporating the calibration metric induced by the
given loss as part of the standard practice for monitoring the training process.

            0.5               Training loss                            95               Training accuracy                                               Train loss
                              Validation loss                                           Validation accuracy                      0.3                    Train CEKL
                                                                                                                                                        Train refinement
            0.4
                                                                       90
                                                                                                                                 0.2
     Loss   0.3
                                                                Acc

                                                                       85                                                        0.1
            0.2


            0.1                                                        80                                                         0
                      0           50       100      150   200                   0          50       100         150        200         0   50     100       150       200
                                          Epochs                                                   Epochs                                        Epochs

             0.2                                                        0.1                                                      0.5
                               Training CEKL                                                                  Training CE22                     Val loss
                               Validation CEKL                                                                Validation CE22
                                                                       0.08                                                      0.4            Val CEKL
            0.15                                                                                                                                Val refinement

                                                                       0.06                                                      0.3
     CEKL    0.1                                                CE22
                                                                       0.04                                                      0.2

            0.05
                                                                       0.02                                                      0.1


                  0                                                         0                                                     0
                          0        50      100      150   200                       0        50      100         150       200         0   50     100       150       200
                                          Epochs                                                    Epochs                                       Epochs


Figure 5: Training and validation trends monitoring loss, accuracy, calibration error and refinement. The
calibration error is an effective tool for detecting overfitting. Observing the loss together with the induced
calibration error and refinement offers unique insights for the performance of the model.


Model selection In practical settings, achieving high accuracy alone is often not sufficient for deploying
machine learning models in decision-making pipelines. Obtaining a low calibration error becomes an equally
important aspect in the evaluation of the model’s performance. In such multi-objective optimization problems,
the Pareto front is a useful tool to determine the set of optimal solutions. Figure 6 shows the Pareto front of
snapshots evaluated at every 10th epoch of training a VGG16 architecture on CIFAR-10 for a total of 250 epochs.
Each point represents the mean and standard error across four seeds. The orange points are Pareto optimal (or
Pareto efficient), meaning that no other snapshots can improve one objective without degrading the other. In
other words, the orange points represent the best possible trade-off between accuracy and calibration error.

Assessing calibration error In this part, we investigate the ranking performance of the class-wise versions of
CE
 c KL and CEd2 via kernel density estimation, and CE with a binned estimator (Kull et al., 2019; Nixon et al.,
               2                                        1
2019). The latter can be seen as the class-wise version of the commonly used ECE (Naeini et al., 2015; Guo
et al., 2017). Specifically, we evaluate calibration error using the three estimators for each of the ten classes
within the CIFAR-10 dataset. The similarity of their performance in terms of ranking the classes can be observed
in Table 5, where the numbers in the brackets represent the ranking order. We used 15 bins with equal-width
binning scheme for CE1 , and the bandwidth for the KDE estimators was set to 0.02. Additionally, Figure 7 show
the corresponding class-wise reliability diagrams for the models evaluated in the table. The blue bars represent
the accuracy per bin. The red bars represent the gap of each bin to perfect calibration, i.e., the difference between
accuracy and confidence for a given bin (darker shades signify under-confidence, while brighter red colors denote
over-confidence).
              Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors




                                                      10
                                                                                                     150
                                       0.015

                                       0.020


                                CEKL
                                       0.025

                                       0.030
                                                                                                           230
                                                                                                            240

                                       0.035

                                       0.040
                                                  82           84       86   88   90            92         94
                                                                         Accuracy

Figure 6: Pareto front of VGG16 snapshots evaluated at every 10th epoch. The model is trained for a total of
250 epochs on CIFAR-10. The orange points Pareto-dominate the rest. The numbers represent the corresponding
epoch. Note that the y−axis is inverted.




Table 5: Calibration error evaluated using three estimators for each of the classes within CIFAR-10. The values
are averaged over four seeds. The numbers in the brackets represent the ranking order.


      Model          Metric     Class 0    Class 1         Class 2     Class 3     Class 4    Class 5       Class 6   Class 7    Class 8    Class 9
                   c KL × 100
                   CE           1.58 (6)   0.91 (1)        2.13 (8)   4.28 (10)    1.78 (7)   3.59 (9)     1.30 (4)   1.09 (2)   1.12 (3)   1.34 (5)
   PreResNet56     d2 × 1000
                   CE           7.25 (6)   4.04 (1)        9.27 (8)   16.96 (10)   8.26 (7)   14.58 (9)    5.34 (3)   5.77 (4)   5.31 (2)   5.99 (5)
                     2
                   CE1 ×1000    6.25 (6)   3.36 (1)        7.65 (8)   15.62 (10)   6.51 (7)   12.76 (9)    4.34 (3)   3.96 (2)   4.52 (4)   4.97 (5)
                   c KL × 100
                   CE           0.86 (5)   0.72 (3)        1.43 (8)   2.76 (10)    0.96 (7)   2.43 (9)     0.71 (2)   0.53 (1)   0.75 (4)   0.93 (6)
 WideResNet28x10   d2 × 1000
                   CE           4.80 (6)   3.65 (2)        7.52 (8)   13.39 (10)   5.22 (7)   11.76 (9)    3.73 (3)   2.91 (1)   4.01 (4)   4.73 (5)
                     2
                   CE1 ×1000    3.47 (5)   2.80 (3)        5.42 (8)   11.61 (10)   3.57 (7)   10.12 (9)    2.50 (2)   1.83 (1)   2.91 (4)   3.49 (6)
                                                                        Popordanoska, Gruber, Tiulpin, Buettner, Blaschko




                                    Class 0                                          Class 1                                         Class 2                                         Class 3                                         Class 4
            1.0                                             1.0                                              1.0                                             1.0                                             1.0
                        Perfect Calibration                              Perfect Calibration                             Perfect Calibration                             Perfect Calibration                             Perfect Calibration

            0.8                                             0.8                                              0.8                                             0.8                                             0.8


                                                            0.6                                              0.6                                             0.6                                             0.6

 Accuracy
            0.6


            0.4                                             0.4                                              0.4                                             0.4                                             0.4


            0.2                                             0.2                                              0.2                                             0.2                                             0.2


            0.0                                             0.0                                              0.0                                             0.0                                             0.0
                  0.0   0.2      0.4      0.6   0.8   1.0         0.0    0.2      0.4      0.6   0.8   1.0         0.0   0.2      0.4      0.6   0.8   1.0         0.0   0.2      0.4      0.6   0.8   1.0         0.0   0.2      0.4      0.6   0.8   1.0
                                    Class 5                                          Class 6                                         Class 7                                         Class 8                                         Class 9
            1.0                                             1.0                                              1.0                                             1.0                                             1.0
                        Perfect Calibration                              Perfect Calibration                             Perfect Calibration                             Perfect Calibration                             Perfect Calibration

            0.8                                             0.8                                              0.8                                             0.8                                             0.8


                                                            0.6                                              0.6                                             0.6                                             0.6

 Accuracy
            0.6


            0.4                                             0.4                                              0.4                                             0.4                                             0.4


            0.2                                             0.2                                              0.2                                             0.2                                             0.2


            0.0                                             0.0                                              0.0                                             0.0                                             0.0
                  0.0   0.2      0.4      0.6   0.8   1.0         0.0    0.2      0.4      0.6   0.8   1.0         0.0   0.2      0.4      0.6   0.8   1.0         0.0   0.2      0.4      0.6   0.8   1.0         0.0   0.2      0.4      0.6   0.8   1.0
                                    Class 0                                          Class 1                                         Class 2                                         Class 3                                         Class 4
            1.0                                             1.0                                              1.0                                             1.0                                             1.0
                        Perfect Calibration                              Perfect Calibration                             Perfect Calibration                             Perfect Calibration                             Perfect Calibration

            0.8                                             0.8                                              0.8                                             0.8                                             0.8


                                                            0.6                                              0.6                                             0.6                                             0.6

 Accuracy
            0.6


            0.4                                             0.4                                              0.4                                             0.4                                             0.4


            0.2                                             0.2                                              0.2                                             0.2                                             0.2


            0.0                                             0.0                                              0.0                                             0.0                                             0.0
                  0.0   0.2      0.4      0.6   0.8   1.0         0.0    0.2      0.4      0.6   0.8   1.0         0.0   0.2      0.4      0.6   0.8   1.0         0.0   0.2      0.4      0.6   0.8   1.0         0.0   0.2      0.4      0.6   0.8   1.0
                                    Class 5                                          Class 6                                         Class 7                                         Class 8                                         Class 9
            1.0                                             1.0                                              1.0                                             1.0                                             1.0
                        Perfect Calibration                              Perfect Calibration                             Perfect Calibration                             Perfect Calibration                             Perfect Calibration

            0.8                                             0.8                                              0.8                                             0.8                                             0.8


                                                            0.6                                              0.6                                             0.6                                             0.6

 Accuracy
            0.6


            0.4                                             0.4                                              0.4                                             0.4                                             0.4


            0.2                                             0.2                                              0.2                                             0.2                                             0.2


            0.0                                             0.0                                              0.0                                             0.0                                             0.0
                  0.0   0.2      0.4     0.6    0.8   1.0         0.0    0.2      0.4     0.6    0.8   1.0         0.0   0.2      0.4     0.6    0.8   1.0         0.0   0.2      0.4     0.6    0.8   1.0         0.0   0.2      0.4     0.6    0.8   1.0
                                 Confidence                                       Confidence                                      Confidence                                      Confidence                                      Confidence



Figure 7: Reliability diagrams for each class of CIFAR-10 using PreResNet56 (top two rows) and WideResNet28x10
(bottom two rows).
