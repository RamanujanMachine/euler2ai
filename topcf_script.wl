(* ::Package:: *)

Get["C:/Users/totos/Documents/Technion/Ramanujan/RISCErgoSum/riscergosum-1.2.3/RISC/Guess.m"];

ComputeTable[summandFunc_, startIndex_: 0, depth_:20, type_:"series"] :=
Module[{k, n},
Table[If[
type=="series",
Sum[summandFunc[k],{k,startIndex,n}],(* use Sum for series *)
Product[summandFunc[k],{k,startIndex,n}]  (* use Product for product *)],
{n,startIndex,depth}]
];

ToPCF[summandFunc_,startIndex_:0,depth_:200,type_:"series", verbose_:False]:=
Module[{data,expressionOfSum,f,n,shiftedExpress,m,k,ak,bk},
data=ComputeTable[summandFunc,startIndex,depth,type];
expressionOfSum=GuessMinRE[data,f[n]];
If[Coefficient[expressionOfSum,f[n+3]]===0,
shiftedExpress=expressionOfSum/. n->(n-2);
k[m_]:=Coefficient[shiftedExpress,f[n]]/. n->m;
ak[m_]:=-Coefficient[shiftedExpress,f[n-1]]/. n->m;
bk[m_]:=-Coefficient[shiftedExpress,f[n-2]]/. n->m;
{
Function[n,Simplify[ak[n]]],
Function[n,Simplify[bk[n]*k[n-1]]],
Function[n,Simplify[k[n]]]
},
If[verbose,Print["Not a continued fraction"]];
{
"NOT_A_CF",
"NOT_A_CF",
"NOT_A_CF"
}
]
];

ExportToPCF[summandFunc_, savePath_, startIndex_:0,depth_:200,type_:"series", verbose_:False]:=
Module[{a,b,inflator, aStr, bStr, inflatorStr, first20Convergents, jsonData},
{a, b, inflator} = ToPCF[summandFunc, startIndex, depth, type, verbose];
aStr = If[a === "NOT_A_CF", a, ToString[a[n], InputForm]];
bStr = If[b === "NOT_A_CF", b, ToString[b[n], InputForm]];
inflatorStr = If[inflator === "NOT_A_CF", inflator, ToString[inflator[n], InputForm]];
first20Convergents = ComputeTable[summandFunc, startIndex, 20+startIndex];
first20Convergents = ToString[#, InputForm] & /@ first20Convergents;
jsonData = <|"a" -> aStr, "b" -> bStr, "inflator" -> inflatorStr,
"func" -> ToString[summandFunc[n], InputForm], "type" -> type, "start" -> startIndex, "first20formula_convergents" -> first20Convergents|>;
Export[savePath, jsonData, "JSON"];]


(* ::Text:: *)
(*Example*)


(*
s[n_] := (-1)^n * (3*n + 1) / 32^n * Sum[Binomial[2*n - 2*k, n - k] * Binomial[2*k, k] * Binomial[n, k]^2, {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/test_recurrence__0__0704.2438__threevariablemahlermeasures.tex__203.json",
	0,
	200,
	"series"
]
*)


(* ::Text:: *)
(*200000 - 349999*)


(* 0 *)
s[k_] := (6 k + 1) * (1/2)^3 / (Factorial[k]^3 * 4^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__0__2101.09753__truncated-d-conj.tex__99.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 1 *)
s[k_] := (-1)^k * (1/2)^3 * k / 1^3 * k * (1 + 4*k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__1__2102.12440__PfaffPiQ2020arXiv.TEX__682.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 2 *)
s[k_] := HypergeometricPFQ[{1/2, 1/2, 1/2}, {1, 1, 1}, k] * (1 + 6*k) / 4^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__2__2102.12440__PfaffPiQ2020arXiv.TEX__856.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 3 *)
s[k_] := HypergeometricPFQ[{1/6, 1/6, 5/6, 5/6}, {1, 1, 1, 3/2}, k] * (5 + 72 k + 108 k^2) / 4^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__3__2102.12440__PfaffPiQ2020arXiv.TEX__918.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 4 *)
s[k_] := HypergeometricPFQ[{{1/2, 1/2}}, {{1, 3/2}}, k] * (1/4)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__4__2102.12440__PfaffPiQ2020arXiv.TEX__932.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 5 *)
s[k_] := HypergeometricPFQ[{1/6, 1/6, 5/6, 5/6}, {1, 3/2, 7/6, 11/6}, k] * (31 + 108 k + 108 k^2) / 4^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__5__2102.12440__PfaffPiQ2020arXiv.TEX__960.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 6 *)
s[k_] := (-1/4)^k * HypergeometricPFQ[{1/2, 1/4, 3/4}, {1, 1, 1}, k] * (3 + 20 k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__6__2102.12440__PfaffPiQ2020arXiv.TEX__1145.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 7 *)
s[k_] := (-1/4)^k * HypergeometricPFQ[{1/2, 1/4, 3/4}, {3/2, 5/4, 7/4}, k] * (5 + 21*k + 20*k^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__7__2102.12440__PfaffPiQ2020arXiv.TEX__1183.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 8 *)
s[k_] := HypergeometricPFQ[{1/2, 1/2, 1/2}, {1, 1, 1}, k] * (5 + 42 k) / 64^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__8__2102.12440__PfaffPiQ2020arXiv.TEX__1371.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 9 *)
s[k_] := HypergeometricSeries[1, {1/2, 1/2, 1/2}, {5/4, 5/4, 7/4, 7/4}, k] * (7 + 42 k + 75 k^2 + 42 k^3) / 64^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__9__2102.12440__PfaffPiQ2020arXiv.TEX__1440.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 10 *)
s[k_] := (2/27)^k * HypergeometricPFQ[{1, 1/2}, {4/3, 5/3}, k] * (3 + 5*k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__10__2102.12440__PfaffPiQ2020arXiv.TEX__1620.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 11 *)
s[k_] := (6 k - 1) * Pochhammer[-1/2, k] * Pochhammer[-1/4, k] / (4^k * Factorial[k]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__11__2103.06416__new_congruences_from_Rahman_summation.tex__668.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 12 *)
s[k_] := HypergeometricSeries[ {3/2, -1/2, -1/2, -1/4, -3/4, 7/6}, {1, 1, 1, 2, 3, 1/6}, k] * (9 - 38 k - 40 k^2) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__12__2103.07872__Pi7F6Double2021arXiv.TEX__883.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 13 *)
s[k_] := HypergeometricSeries[ {1/6, -1/6, 5/6, -5/6, 7/6, 5/12, 11/12, 19/18}, {1, 1, 1/2, 3/2, 1/3, 2/3, -2/3, 1/18}, k] * (2160*k^3 - 972*k^2 - 660*k + 175) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__13__2103.07872__Pi7F6Double2021arXiv.TEX__1321.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 14 *)
s[k_] := Hypergeometric[{-1/6, 7/6, -7/6, 13/6, -13/6, -5/12, 1/12, 11/18}, {1, 1, 1/2, 3/2, -1/3, -2/3, 2/3, -7/18}, k] * (2160*k^3 - 756*k^2 - 1668*k + 65) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__14__2103.07872__Pi7F6Double2021arXiv.TEX__1345.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 15 *)
s[k_] := HypergeometricSeries[1/2, 1/4, 3/4, 1/8, 5/8, 1, 1, 1, 7/8, 11/8, k] * (480 k^2 + 212 k + 15) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__15__2103.07872__Pi7F6Double2021arXiv.TEX__1429.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 16 *)
s[k_] := HypergeometricSeries[1/2, 1/4, 3/4, 3/8, 7/8, 1, 1, 1, 9/8, 13/8, k] * (640*k^3 + 560*k^2 + 112*k + 7) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__16__2103.07872__Pi7F6Double2021arXiv.TEX__1439.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 17 *)
s[k_] := Hypergeometric[{-1/2, 1/4, -1/4, -1/8, -5/8}, {1, 1, 1, 1/8, 5/8}, k] * (960*k^3 - 232*k^2 - 38*k + 5) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__17__2103.07872__Pi7F6Double2021arXiv.TEX__1580.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 18 *)
s[k_] := Hypergeometric[{-3/2, 5/4, -5/4, -1/8, -5/8}, {1, 1, 1, 1/8, -3/8}, k] * (960*k^3 - 232*k^2 - 710*k + 75) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__18__2103.07872__Pi7F6Double2021arXiv.TEX__1630.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 19 *)
s[k_] := Hypergeometric[{-1/2, -1/4, 1/8, -3/8}, {1/2, 3/4, 9/8, 13/8}, k] * (1 - 7*k + 40*k^2) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__19__2103.07872__Pi7F6Double2021arXiv.TEX__1666.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 20 *)
s[k_] := Hypergeometric[{-1/2, 1/4, -1/8, -5/8}, {1/2, 9/4, 7/8, 11/8}, k] * (120 k^2 + 77 k + 5) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__20__2103.07872__Pi7F6Double2021arXiv.TEX__1675.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 21 *)
s[k_] := Hypergeometric[-1/2, 1/4, -1/8, 3/8, 1/2, 5/4, 7/8, 11/8, k] * (1 + 11*k + 106*k^2 + 240*k^3) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__21__2103.07872__Pi7F6Double2021arXiv.TEX__1684.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 22 *)
s[k_] := (1/16)^k * (4/(8*k + 1) - 2/(8*k + 4) - 1/(8*k + 5) - 1/(8*k + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__22__2103.07872__Pi7F6Double2021arXiv.TEX__1855.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 23 *)
s[k_] := Hypergeometric2F1[1/2, 3/4, 1/8, 5/8, k] * (120 k^2 + 151 k + 47) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__23__2103.07872__Pi7F6Double2021arXiv.TEX__1865.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 24 *)
s[k_] := HypergeometricPFQ[{1/2, 3/4, 1/8, -3/8}, {5/2, 11/4, 9/8, 13/8}, k] * (120 k^2 + 235 k + 99) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__24__2103.07872__Pi7F6Double2021arXiv.TEX__1875.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 25 *)
s[k_] := Hypergeometric[{-1/2, -1/4, -3/8, -7/8}, {1/2, 7/4, 5/8, 9/8}, k] * (480*k^2 - 172*k - 9) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__25__2103.07872__Pi7F6Double2021arXiv.TEX__1885.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 26 *)
s[k_] := Hypergeometric[-1/2, -5/4, -7/8, -11/8, 1/2, 11/4, 1/8, 5/8, k] * (160*k^2 - 36*k - 13) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__26__2103.07872__Pi7F6Double2021arXiv.TEX__1905.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 27 *)
s[k_] := (1/16)^k * (8/(8*k + 2) + 4/(8*k + 3) + 4/(8*k + 4) - 1/(8*k + 7));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__27__2103.07872__Pi7F6Double2021arXiv.TEX__1917.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 28 *)
s[k_] := HypergeometricPFQ[{-1/2, 1/4, -5/8, -9/8}, {5/2, 9/4, 3/8, 7/8}, k] * (19 - 62*k - 80*k^2) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__28__2103.07872__Pi7F6Double2021arXiv.TEX__1933.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 29 *)
s[k_] := Hypergeometric[-1/2, -3/4, -1/8, -5/8, 1/2, 1/4, 7/8, 11/8, k] * (160 k^2 - 108 k + 21) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__29__2103.07872__Pi7F6Double2021arXiv.TEX__1941.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 30 *)
s[k_] := Hypergeometric[{-1/2, -3/4, -5/8, -9/8}, {1/2, 9/4, 3/8, 7/8}, k] * (11 + 260 k - 480 k^2) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__30__2103.07872__Pi7F6Double2021arXiv.TEX__1951.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 31 *)
s[k_] := HypergeometricPFQ[{1/2, 1/4, 3/8, 7/8}, {3/2, 5/4, 11/8, 15/8}, k] * (65 + 413 k + 812 k^2 + 480 k^3) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__31__2103.07872__Pi7F6Double2021arXiv.TEX__1961.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 32 *)
s[q_] := (-1)^q * Factorial[6*q] * (545140134*q + 13591409) / (Factorial[3*q] * Factorial[q]^3 * (640320)^(3*q + 3/2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__32__2103.09654__RamanujanInComputing.tex__229.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 33 *)
s[n_] := 1/(n*4^n) * Binomial[2*n, n];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__33__2103.11960__New_series_with_Cauchy_and_Stirling_numbers,_Part_2.tex__277.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 34 *)
s[k_] := (-1/27)^k * HypergeometricPFQ[{1, 1/2, 2/3}, {4/3, 4/3, 4/3}, k] * (3 + 7*k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__34__2104.01599__Pi7F6Triple2021arXiv.TEX__953.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 35 *)
s[k_] := HypergeometricSeries[{1, 1/2, 1/3, 1/4, 3/4, 5/6}, {5/3, 5/3, 5/3, 7/6, 7/6, 7/6}, k] * (4368*k^4 + 9742*k^3 + 7799*k^2 + 2588*k + 283) / 729^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__35__2104.01599__Pi7F6Triple2021arXiv.TEX__968.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 36 *)
s[k_] := (-1/27)^k * HypergeometricPFQ[{1/2, 1, 3}, {5/2, 5/3, 7/3}, 17 + 14*k];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__36__2104.01599__Pi7F6Triple2021arXiv.TEX__1028.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 37 *)
s[k_] := ((-1)/27)^k * HypergeometricPFQ[{3/2, 1, 3}, {7/2, 7/3, 8/3}, k] * (63 + 59*k + 14*k^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__37__2104.01599__Pi7F6Triple2021arXiv.TEX__1046.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 38 *)
s[k_] := (-1/27)^k * HypergeometricPFQ[{3, 1/2, -2/3}, {2/3, 5/3, 5/3}, k] * (13 + 21*k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__38__2104.01599__Pi7F6Triple2021arXiv.TEX__1286.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 39 *)
s[k_] := (-1/27)^k * HypergeometricPFQ[{3, 1/2, 2/3}, {4/3, 7/3, 7/3}, k] * (23 + 21*k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__39__2104.01599__Pi7F6Triple2021arXiv.TEX__1296.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 40 *)
s[k_] := (-1/27)^k * HypergeometricPFQ[{1, 1/2, -2/3}, {2/3, 2/3, 5/3}, k] * k * (13 + 21*k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__40__2104.01599__Pi7F6Triple2021arXiv.TEX__1306.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 41 *)
s[k_] := (-1/27)^k * HypergeometricPFQ[{1, 1/2, -4/3}, {1/3, 1/3, 4/3}, k] * (21 k^2 + 8 k - 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__41__2104.01599__Pi7F6Triple2021arXiv.TEX__1315.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 42 *)
s[k_] := (-1/27)^k * HypergeometricPFQ[{1, 1/2, 1/3}, {5/3, 5/3, 5/3}, k] * (9 + 28*k + 21*k^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__42__2104.01599__Pi7F6Triple2021arXiv.TEX__1325.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 43 *)
s[k_] := (-1/27)^k * HypergeometricPFQ[{3, 1/2, -4/3}, {1/3, 4/3, 7/3}, k] * (5 + 3*k) * (8 + 21*k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__43__2104.01599__Pi7F6Triple2021arXiv.TEX__1335.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 44 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__44__2104.12412__Ramanujan_series_for_pi.tex__131.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 45 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__45__2104.12412__Ramanujan_series_for_pi.tex__131.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 46 *)
s[k_] := Factorial[2 k]^3 / (Factorial[k]^6) * (5 + 7 * 6 * k) / 64^(2 k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__46__2104.12412__Ramanujan_series_for_pi.tex__453.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 47 *)
s[n_] := ((-1)^n * Factorial[6 n] * (545140134 n + 13591409)) / (Factorial[3 n] * (Factorial[n])^3 * (640320^(3 n + 3/2)));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__47__2104.12412__Ramanujan_series_for_pi.tex__539.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 48 *)
s[k_] := (-1)^k * Factorial[6 k] / (Factorial[3 k] * Factorial[k]^3) * (13591409 + 163 * 3344418 * k) / 640320^(3 * (k + 1/2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__48__2104.12412__Ramanujan_series_for_pi.tex__539.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 49 *)
s[k_] := (4 k + 1) Binomial[2 k, k]^3 / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__49__2105.05567__rat-sum-vv.tex__340.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 50 *)
s[k_] := (4 k - 1) k / (2 k - 1)^2 * Binomial[2 k, k]^3 / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__50__2105.05567__rat-sum-vv.tex__366.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 51 *)
s[k_] := ((4 k + 3) (2 k + 1) / (k + 1)^2) * Binomial[2 k, k]^3 / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__51__2105.05567__rat-sum-vv.tex__380.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 52 *)
s[k_] := (4 k + 1)/((k + 1) (2 k - 1)) * Binomial[2 k, k]^3 / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__52__2105.05567__rat-sum-vv.tex__385.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 53 *)
s[k_] := (4 k + 3)/((k + 1)^3) * Binomial[2 k, k]^3 / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__53__2105.05567__rat-sum-vv.tex__390.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 54 *)
s[k_] := (4 k - 1) / ((2 k - 1)^3) * Binomial[2 k, k]^3 / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__54__2105.05567__rat-sum-vv.tex__390.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 55 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__55__2105.05809___03_Zeta_2.tex__362.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 56 *)
s[k_] := Pi * (-1)^k / k * Sum[1 / (2 * ell + 2 * k + 1), {ell, 0, Infinity}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__56__2105.11771__Involve.tex__886.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 57 *)
s[k_] := 1/(k^2 + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__57__2106.13905__document.tex__1071.json",
	-oo,
	200,
	"series"
];

ClearAll[n];

(* 58 *)
s[k_] := HypergeometricSeries[1/2, -1/2, 3/2, 1/4, 3/4, 1] * (80 k^3 + 148 k^2 + 80 k + 9) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__58__2108.12796__JacksonPiQ2021X.TEX__1099.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 59 *)
s[n_] := HypergeometricSeries[1/2, 1/2, 3/2, 3/4, 5/4, n] * (240 n^3 + 532 n^2 + 336 n + 45) / 16^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__59__2108.12796__JacksonPiQ2021X.TEX__1127.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 60 *)
s[n_] := HypergeometricSeries[1/2, 3/4, 1/8, 5/8, 3/2, 7/4, 9/8, 13/8, n] * (120 n^2 + 151 n + 47) / 16^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__60__2108.12796__JacksonPiQ2021X.TEX__1367.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 61 *)
s[k_] := HypergeometricPFQ[{1/2, 3/4, 1/8, -3/8}, {5/2, 11/4, 9/8, 13/8}, k] * (120 k^2 + 235 k + 99) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__61__2108.12796__JacksonPiQ2021X.TEX__1388.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 62 *)
s[n_] := HypergeometricSeries[1/2, 1/4, 3/4, 1/8, 5/8, 1, 1, 1, 7/8, 11/8, n] * (480 n^2 + 212 n + 15) / 16^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__62__2108.12796__JacksonPiQ2021X.TEX__1451.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 63 *)
s[n_] := HypergeometricSeries[1/2, 1/4, 3/4, 3/8, 7/8, 1, 1, 1, 9/8, 13/8, n] * (640 n^3 + 560 n^2 + 112 n + 7) / 16^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__63__2108.12796__JacksonPiQ2021X.TEX__1473.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 64 *)
s[k_] := Hypergeometric[{-1/2, -1/4, 1/8, -3/8}, {1/2, 3/4, 9/8, 13/8}, k] * (40*k^2 - 7*k + 1) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__64__2108.12796__JacksonPiQ2021X.TEX__1682.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 65 *)
s[k_] := Hypergeometric[{-1/2, 1/4, -1/8, -5/8}, {1/2, 9/4, 7/8, 11/8}, k] * (120 k^2 + 77 k + 5) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__65__2108.12796__JacksonPiQ2021X.TEX__1704.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 66 *)
s[k_] := HypergeometricHarmonicNumber[-1/2, 1/4, -5/8, -9/8, 5/2, 9/4, 3/8, 7/8, k] * (19 - 62*k - 80*k^2) / 16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__66__2108.12796__JacksonPiQ2021X.TEX__1775.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 67 *)
s[n_] := (-1/27)^n * HypergeometricPFQ[{1, 1/2, -2/3}, {2/3, 2/3, 5/3}, n] * n * (13 + 21*n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__67__2108.12796__JacksonPiQ2021X.TEX__2270.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 68 *)
s[n_] := (-1/27)^n * HypergeometricPFQ[{1, 1/2, 2/3}, {4/3, 4/3, 4/3}, n] * (3 + 7*n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__68__2108.12796__JacksonPiQ2021X.TEX__2328.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 69 *)
s[n_] := (-1/27)^n * HypergeometricPFQ[{1, 1/2, 1/3}, {5/3, 5/3, 5/3}, n] * (9 + 28*n + 21*n^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__69__2108.12796__JacksonPiQ2021X.TEX__2352.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 70 *)
s[n_] := (-1/27)^n * HypergeometricPFQ[{1/2, 1, 3}, {5/2, 5/3, 7/3}, 17 + 14*n];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__70__2108.12796__JacksonPiQ2021X.TEX__2515.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 71 *)
s[n_] := (-1/27)^n * HypergeometricPFQ[{3, 1/2, 2/3}, {4/3, 7/3, 7/3}, n] * (23 + 21*n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__71__2108.12796__JacksonPiQ2021X.TEX__2589.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 72 *)
s[k_] := (-1/27)^k * HypergeometricPFQ[{3, 1/2, -2/3}, {2/3, 5/3, 5/3}, k] * (13 + 21*k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__72__2108.12796__JacksonPiQ2021X.TEX__2612.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 73 *)
s[k_] := (k/(k + 1))^((-1)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__73__2109.01477__Mizuno-type_formula7.tex__377.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 74 *)
s[k_] := (6 k + 1)/(256^k) * Binomial[2 k, k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__74__2109.09877__MaoSun256.tex__127.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 75 *)
s[k_] := (198 k^2 - 425 k + 210) * (k^3 * Binomial[2 k, k]^3) / 4096^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__75__2110.03651__NewSeries.tex__118.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 76 *)
s[k_] := (4 k + 1) / ((-64)^k * Binomial[2 k, k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__76__2110.03651__NewSeries.tex__129.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 77 *)
s[k_] := (17439700 k^2 - 47250409 k + 8929776) * 81^(k - 1) / (Binomial[2 k, k + 1]^2 * Binomial[4 k, 2 k + 1]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__77__2110.03651__NewSeries.tex__244.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 78 *)
s[k_] := k * Factorial[k]^4 / 36^k * (40 * k^2 - 42 * k - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__78__2110.03651__NewSeries.tex__296.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 79 *)
s[k_] := k Binomial[2 k, k] (1365 k^2 + 575 k + 86) / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__79__2110.03651__NewSeries.tex__314.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 80 *)
s[k_] := Binomial[2 k, k]^3 / 256^k * (6 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__80__2110.03651__NewSeries.tex__378.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 81 *)
s[k_] := ((k^2 + 1) * Binomial[2 k, k]^3 / 256^k) * (192 k^2 - 626 k - 103);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__81__2110.03651__NewSeries.tex__396.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 82 *)
s[k_] := (30 k^2 + 3 k - 2) * Binomial[2 k, k]^3 / ((2 k - 1)^3 * (-512)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__82__2110.03651__NewSeries.tex__451.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 83 *)
s[k_] := Binomial[2 k, k]^3 / 4096^k * (42 k + 5);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__83__2110.03651__NewSeries.tex__485.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 84 *)
s[k_] := Binomial[2 k, k]^3 * (5 (6 k + 1) + 12 k) / 4096^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__84__2110.03651__NewSeries.tex__489.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 85 *)
s[k_] := (k * Binomial[2 k, k]^3 / 4096^k) * (210 k^2 - 5 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__85__2110.03651__NewSeries.tex__492.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 86 *)
s[k_] := (k^2 * Binomial[2 k, k]^3 / 4096^k) * (504 k^2 - 314 k - 11);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__86__2110.03651__NewSeries.tex__494.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 87 *)
s[k_] := (k^2 * Binomial[2 k, k]^3 / 4096^k) * (11 * 504 * k^3 - (11 * 1036 + 504) * k^2 + (11 * 506 + 314) * k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__87__2110.03651__NewSeries.tex__496.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 88 *)
s[k_] := (42 k^2 - 3 k - 1) / (4096^k) * (2/k * Binomial[2 (k - 1), k - 1])^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__88__2110.03651__NewSeries.tex__503.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 89 *)
s[k_] := (42 (k + 1)^2 - 3 (k + 1) - 1)/(4096^k) * Binomial[2 k, k]^3 / (k + 1)^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__89__2110.03651__NewSeries.tex__503.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 90 *)
s[k_] := Binomial[2 k, k]^3 * (42 k^2 + 81 k + 38) / ((k + 1)^3 * 4096^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__90__2110.03651__NewSeries.tex__507.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 91 *)
s[k_] := (Binomial[2 k, k]^3 * (2128 k^2 + 4050 k + 1861)) / ((k + 1)^3 * 4096^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__91__2110.03651__NewSeries.tex__514.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 92 *)
s[k_] := (k^2 * Binomial[2*k, k]^3 * (78162*k^2 + 145175*k + 64431)) / ((k + 1)^3 * 4096^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__92__2110.03651__NewSeries.tex__522.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 93 *)
s[k_] := (8242975 k^2 + 16441878 k + 8198387) * Binomial[2 k, k + 1]^2 * Binomial[4 k, 2 k] / (-63^2)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__93__2110.03651__NewSeries.tex__977.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 94 *)
s[k_] := ((2428400 k^2 - 5044368 k + 2584321) * k^3 * Binomial[2 k, k]^2 * Binomial[4 k, 2 k]) / ((-2^10 * 3^4)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__94__2110.03651__NewSeries.tex__989.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 95 *)
s[k_] := (2475740800 k^2 + 4950772932 k + 2475031103) * Binomial[2 k, k + 1]^2 * Binomial[4 k, 2 k] / ((-2^10 * 3^4)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__95__2110.03651__NewSeries.tex__992.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 96 *)
s[k_] := (1967513600 k^2 + 3935104168 k + 1967590547) * Binomial[2 k, k + 1]^2 * Binomial[4 k, 2 k] / 28^(4 k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__96__2110.03651__NewSeries.tex__996.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 97 *)
s[k_] := (643835623600 k^2 - 1361740501968 k + 711617288021) * k^3 * Binomial[2 k, k]^2 * Binomial[4 k, 2 k] / ((-2^10 * 21^4)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__97__2110.03651__NewSeries.tex__1006.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 98 *)
s[k_] := (4941882 k^2 + 9895613 k + 4953661) * Binomial[2 k, k + 1] * Binomial[3 k, k + 1] * Binomial[6 k, 3 k] / (2 * 30^3)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__98__2110.03651__NewSeries.tex__1097.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 99 *)
s[k_] := (6802059888 k^2 + 13603203918 k + 6801143345) * Binomial[2 k, k + 1] * Binomial[3 k, k + 1] * Binomial[6 k, 3 k] / ((-96)^(3 k));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__99__2110.03651__NewSeries.tex__1104.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 100 *)
s[k_] := (3054600 k^2 - 16826114 k + 11236485) / ((-256)^k * k^3 * Binomial[2 k, k]^2 * T_k[1, 16]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__100__2110.03651__NewSeries.tex__1353.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 101 *)
s[k_] := (357600 k^2 - 239434 k + 401075) / ((-1024)^k * k^3 * Binomial[2 k, k]^2 * T_k[34, 1]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__101__2110.03651__NewSeries.tex__1355.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 102 *)
s[k_] := k * (133120*k^2 - 28704*k + 2669) / ((-168^2)^k * Binomial[2*k, k] * Binomial[4*k, 2*k] * T_k[7, 4096]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__102__2110.03651__NewSeries.tex__1411.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 103 *)
s[k_] := (148778208 k^2 - 813461721 k + 717359335) / ((-100)^k * k^3 * S[k, 1, 25]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__103__2110.03651__NewSeries.tex__1744.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 104 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__104__2110.07457__ASWSurvey0111.tex__867.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 105 *)
s[n_] := (1/(4^n) * Binomial[2*n, n])^2 / (n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__105__2111.10998__Apery-AMtVs-04122022.tex__677.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 106 *)
s[n_] := (1/(4^n) * Binomial[2*n, n])^2 / (n + 1)^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__106__2111.10998__Apery-AMtVs-04122022.tex__677.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 107 *)
s[n_] := (1/(4^n) * Binomial[2*n, n])^2 / (2*n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__107__2111.10998__Apery-AMtVs-04122022.tex__820.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 108 *)
s[n_] := 1/(4^n (2 n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__108__2111.10998__Apery-AMtVs-04122022.tex__946.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 109 *)
s[j_] := 2^(j + 1) / ((2*j + 1) Binomial[2*j, j]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__109__2112.00622__fibonacci-with-inverse-binomial-v6.tex__620.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 110 *)
s[k_] := 1 / (4*k^2 - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__110__2112.08020__Creative_proofs_in_combinations.tex__271.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 111 *)
s[k_] := 1/k^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__111__2202.10615__On Average-Case Error Bounds for Kernel-Based Bayesian Quadrature_slash_se.tex__259.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 112 *)
s[k_] := 1/k^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__112__2202.10615__se.tex__259.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 113 *)
s[k_] := (4/(8 k + 1) - 2/(8 k + 4) - 1/(8 k + 5) - 1/(8 k + 6)) * 1/16^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__113__2203.02631__TWF_51-100_arxiv_2.tex__5373.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 114 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__114__2203.09465__Pi_over_3.tex__135.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 115 *)
s[n_] := 1 / (n * (2*n - 1) * (4*n - 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__115__2203.09465__Pi_over_3.tex__143.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 116 *)
s[k_] := (-1)^(k + 1) / (2 k - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__116__2203.09465__Pi_over_3.tex__204.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 117 *)
s[n_] := 3 / (4 n (4 n - 2) (4 n - 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__117__2203.09465__Pi_over_3.tex__236.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 118 *)
s[n_] := 1 / (n * (2*n - 1) * (4*n - 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__118__2203.09465__Pi_over_3.tex__240.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 119 *)
s[k_] := 1 / ((4 k - 1) (4 k - 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__119__2203.09465__Pi_over_3.tex__301.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 120 *)
s[k_] := 1 / ((4 k + 1) (4 k - 1) (4 k - 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__120__2203.09465__Pi_over_3.tex__335.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 121 *)
s[k_] := 1 / ((2 k + 1) (2 k - 1) (4 k + 1) (4 k - 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__121__2203.09465__Pi_over_3.tex__378.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 122 *)
s[k_] := (4 k + 1) Binomial[2 k, k]^3 / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__122__2203.16047__qRationalReduction_22.7.31b_.tex__704.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 123 *)
s[k_] := (2*k + 1)*(4*k + 3)* Binomial[2*k, k]^3 / ((k + 1)^2 * (-64)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__123__2203.16047__qRationalReduction_22.7.31b_.tex__711.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 124 *)
s[k_] := (4 k + 1) Binomial[2 k, k]^3 / ((2 k - 1) (k + 1) (-64)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__124__2203.16047__qRationalReduction_22.7.31b_.tex__711.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 125 *)
s[k_] := (4 k - 1) / ((2 k - 1)^3) * Binomial[2 k, k]^3 / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__125__2203.16047__qRationalReduction_22.7.31b_.tex__711.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 126 *)
s[k_] := k*(4*k - 1)/((2*k - 1)^2)*Binomial[2*k, k]^3/(-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__126__2203.16047__qRationalReduction_22.7.31b_.tex__711.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 127 *)
s[k_] := (6 k + 1) * Binomial[2 k, k]^3 / 256^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__127__2203.16047__qRationalReduction_22.7.31b_.tex__885.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 128 *)
s[k_] := (12 k^2 - 1) * Binomial[2 k, k]^3 / ((2 k - 1)^2 * 256^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__128__2203.16047__qRationalReduction_22.7.31b_.tex__890.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 129 *)
s[k_] := k*(6*k - 1)/((2*k - 1)^3)*Binomial[2*k, k]^3/(256^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__129__2203.16047__qRationalReduction_22.7.31b_.tex__895.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 130 *)
s[k_] := (2^(2 k) / (k Binomial[2 k, k]))^2 / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__130__2204.04535__TG_RF_KA_Fibonacci-Catalan-series_20220409.tex__722.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 131 *)
s[k_] := Binomial[2 k, k]^2 / (2^(4 k + 1) * (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__131__2204.04535__TG_RF_KA_Fibonacci-Catalan-series_20220409.tex__764.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 132 *)
s[k_] := Binomial[2 k, k] * Binomial[2 k + 2, k + 1] / (2^(4 k + 3) * (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__132__2204.04535__TG_RF_KA_Fibonacci-Catalan-series_20220409.tex__768.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 133 *)
s[k_] := Binomial[2 k, k]^2 / (2^(4 k + 2) * (k + 1) * (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__133__2204.04535__TG_RF_KA_Fibonacci-Catalan-series_20220409.tex__780.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 134 *)
s[k_] := Binomial[2 k, k] * Binomial[2 k + 2, k + 1] / (2^(4 k + 4) * (k + 1) * (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__134__2204.04535__TG_RF_KA_Fibonacci-Catalan-series_20220409.tex__784.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 135 *)
s[k_] := Pochhammer[1/2, k] * Pochhammer[1, k] * Pochhammer[1, k] / (Pochhammer[3/2, k] * Pochhammer[3/2, k] * Factorial[k]) * (-1/4)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__135__2204.05647__Combinatorial_summation.tex__736.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 136 *)
s[t_] := P[0, t, bypass, 0];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__136__2204.07861__article.tex__157.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 137 *)
s[t_] := P[0, t, bypass, 0];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__137__2204.07861__article.tex__292.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 138 *)
s[k_] := (25 k - 3) / (2^k Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__138__2204.08275__P80.tex__167.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 139 *)
s[k_] := (30 k - 7) (-2)^k / Binomial[4 k, 2 k];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__139__2204.08275__P80.tex__376.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 140 *)
s[k_] := k * (126*k + 29) * (-2)^k / Binomial[4*k, 2*k];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__140__2204.08275__P80.tex__445.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 141 *)
s[k_] := (7 k - 3) * 8^k / (k * (2 k - 1) * 3^k * Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__141__2204.08275__P80.tex__445.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 142 *)
s[k_] := (6 k - 1) * (-2)^(k - 1) / (k * (2 k - 1) * Binomial[4 k, 2 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__142__2204.08275__P80.tex__445.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 143 *)
s[k_] := (14 k - 3) / (k (2 k - 1) 4^k Binomial[4 k, 2 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__143__2204.08275__P80.tex__445.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 144 *)
s[k_] := (12 k - 5) * 4^k / ((2 k - 1) * Binomial[4 k, 2 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__144__2204.08275__P80.tex__887.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 145 *)
s[k_] := (12 k - 5) 4^k / ((2 k - 1) Binomial[4 k, 2 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__145__2204.08275__P80.tex__890.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 146 *)
s[k_] := (k*(12*k - 5) - 3*(3*k - 1)) / (k*(2*k - 1)*Binomial[4*k, 2*k])*4^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__146__2204.08275__P80.tex__896.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 147 *)
s[k_] := (3*(2*k - 1)*(30*k - 7) - (18*k + 1)) / ((2*k - 1) Binomial[4*k, 2*k]) * (-2)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__147__2204.08275__P80.tex__902.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 148 *)
s[k_] := (18 k + 1) * (-2)^k / ((2 k - 1) * Binomial[4 k, 2 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__148__2204.08275__P80.tex__906.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 149 *)
s[k_] := (6 k - 1) * (-2)^k / (k * (2 k - 1) * Binomial[4 k, 2 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__149__2204.08275__P80.tex__912.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 150 *)
s[k_] := 1/16^k * (4/(8*k + 1) - 2/(8*k + 4) - 1/(8*k + 5) - 1/(8*k + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__150__2205.08617__BBP_v3.tex__54.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 151 *)
s[k_] := 1/16^k * (47 + 151*k + 120*k^2) / (15 + 194*k + 712*k^2 + 1024*k^3 + 512*k^4);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__151__2205.08617__BBP_v3.tex__60.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 152 *)
s[k_] := (1 + 2/k)^(k*(-1)^(k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__152__2205.09492__kuro.tex__189.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 153 *)
s[k_] := k^2 * (k - 1) * (9*k + 1) * BellB[k] / ((-32)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__153__2205.11129__Polynomial_reductions_for_holonomic_functions_0627.tex__430.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 154 *)
s[k_] := k^2 * (k - 1) * (9*k + 1) * BellB[k] / ((-32)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__154__2205.11129__Polynomial_reductions_for_holonomic_functions_0627.tex__459.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 155 *)
s[k_] := (k^2 + k + 1) * (126*k^2 + 41*k + 5) * Bell[k] / (-32)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__155__2205.11129__Polynomial_reductions_for_holonomic_functions_0627.tex__562.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 156 *)
s[k_] := (1/16)^k * Binomial[2*k, k]^2 * (1/(2*k - 1)^3 - 1/(2*k - 1)^2 + 1/(2*k - 1) - 1/(2*k));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__156__2206.05026__OddSquaredV47.tex__320.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 157 *)
s[k_] := (1/16)^k * Binomial[2*k, k]^2 / ((2*k - 1)^3 * (2*k));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__157__2206.05026__OddSquaredV47.tex__320.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 158 *)
s[k_] := 2*(1/16)^k * Binomial[2*k, k]^2 / ((2*k - 1)^3 * (2*k)) + 2*Sum[(1/16)^k * Binomial[2*k, k]^2 / ((2*k - 1)^3 * (2*m)), {m, 1, k - 1}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__158__2206.05026__OddSquaredV47.tex__330.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 159 *)
s[k_] := (1/16)^k * Binomial[2*k, k]^2 / (2*k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__159__2206.05026__OddSquaredV47.tex__429.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 160 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__160__2206.07174__9001.tex__85.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 161 *)
s[n_] := (-1)^(n + 1) * (1/(n + 1) + 1/n - 4/(2*n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__161__2206.07174__9001.tex__90.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 162 *)
s[k_] := (-1)^(k + 1) / (k * (2*k + 1) * (k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__162__2206.07174__9001.tex__90.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 163 *)
s[n_] := 3 / (n * (n + 1) * (4*n + 1) * (4*n + 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__163__2206.07174__9001.tex__98.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 164 *)
s[r_] := Binomial[r - 1/2, r] * Pochhammer[1/2, r] / Pochhammer[3/2, r];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__164__2207.05551__UMGaussian_arxiv.tex__554.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 165 *)
s[k_] := 1/16^k * (4/(8*k + 1) - 2/(8*k + 4) - 1/(8*k + 5) - 1/(8*k + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__165__2208.07696__paper.tex__111.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 166 *)
s[k_] := (-1)^k * (4*k + 1) * (1/2)^(k^3) / Factorial[k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__166__2210.01331__On_some_double_series_for_pi.tex__101.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 167 *)
s[k_] := (6 k + 1) * (1/2)^3 / (Factorial[k]^3 * 4^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__167__2210.01331__On_some_double_series_for_pi.tex__109.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 168 *)
s[k_] := (6*k + 1) * (1/2)^3 * Factorial[k]^-3 * 4^-k * Sum[1/(2*j - 1)^2 - 1/(16*j^2), {j, 1, k}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__168__2210.01331__On_some_double_series_for_pi.tex__130.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 169 *)
s[k_] := (-1)^k * (4*k + 1) * (1/2)^(k^3) / (Factorial[k]^3) * Sum[(-1)^i / i^2, {i, 1, 2*k}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__169__2210.01331__On_some_double_series_for_pi.tex__150.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 170 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1) * 16^k) * (Harmonic[2 k, 2] - 1/4 * Harmonic[k, 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__170__2210.07238__234s.tex__176.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 171 *)
s[k_] := (6 k + 1) * Binomial[2 k, k]^3 / 256^k * (Harmonic[2 k, 2] - 5/16 * Harmonic[k, 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__171__2210.07238__234s.tex__207.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 172 *)
s[k_] := (4 k + 1) Binomial[2 k, k]^3 / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__172__2210.07238__234s.tex__211.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 173 *)
s[k_] := (4*k + 1) * Binomial[2*k, k]^3 / (-64)^k * Sum[(-1)^j / j^2, {j, 1, 2*k}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__173__2210.07238__234s.tex__217.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 174 *)
s[k_] := (4 k + 1) * Binomial[2 k, k]^3 / (-64)^k * (Harmonic[2 k, 2] - 1/2 * Harmonic[k, 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__174__2210.07238__234s.tex__222.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 175 *)
s[k_] := (25 k - 3) / (2^k * Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__175__2210.07238__234s.tex__365.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 176 *)
s[k_] := (42 k + 5) * Binomial[2 k, k]^3 / 4096^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__176__2210.07238__234s.tex__1016.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 177 *)
s[k_] := (42 k + 5) * Binomial[2 k, k]^3 / 4096^k * (Harmonic[2 k, 2] - 25/92 * Harmonic[k, 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__177__2210.07238__234s.tex__1030.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 178 *)
s[k_] := (20 k + 3) * Binomial[2 k, k]^2 * Binomial[4 k, 2 k] / (-1024)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__178__2210.07238__234s.tex__1100.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 179 *)
s[k_] := Binomial[2 k, k]^4 * Binomial[3 k, k] / 4096^k * ((74 k^2 + 27 k + 3) * (51 HarmonicNumber[3 k] + 250 HarmonicNumber[2 k] - 153 HarmonicNumber[k]) + 15);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__179__2210.07238__234s.tex__1347.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 180 *)
s[k_] := Binomial[2 k, k]^2 * Binomial[3 k, k]^2 * Binomial[6 k, 3 k] / 10^(6 k) * (3 * (532 k^2 + 126 k + 9) * (HarmonicNumber[6 k] - HarmonicNumber[k]) + 532 k + 63);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__180__2210.07238__234s.tex__1446.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 181 *)
s[k_] := Binomial[2 k, k]^3 * Binomial[4 k, 2 k] * Binomial[8 k, 4 k] / (2^18 * 7^4)^k * ((1920 k^2 + 304 k + 15) * HarmonicNumber[k] + 1920 k + 152);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__181__2210.07238__234s.tex__1536.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 182 *)
s[k_] := Binomial[2 k, k]^7 / 2^(20 k) * (7 * (168 k^3 + 76 k^2 + 14 k + 1) * (Harmonic[2 k] - Harmonic[k]) + 252 k^2 + 76 k + 7);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__182__2210.07238__234s.tex__1579.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 183 *)
s[k_] := Binomial[2 k, k]^7 / 2^(20 k) * ((168 k^3 + 76 k^2 + 14 k + 1) * (16 HarmonicNumber[2 k, 2] - 5 HarmonicNumber[k, 2]) + 8 (6 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__183__2210.07238__234s.tex__1595.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 184 *)
s[k_] := 1 - 1/(4 k^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__184__2210.09123__Fourier.tex__337.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 185 *)
s[k_] := 1 - 1/(36 k^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__185__2210.09123__Fourier.tex__373.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 186 *)
s[k_] := (2 k/(2 k - 1))*(2 k/(2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__186__2210.09123__Fourier.tex__379.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 187 *)
s[k_] := 1 - 1/(2 k + 1)^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__187__2210.09123__Fourier.tex__385.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 188 *)
s[n_] := (1/(2 n))^(2/(2 n - 1)) * Product[(2 k)^(2 k)/((2 k - 1)^(2 k - 1)), {k, 1, n}]^(4/(4 n^2 - 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__188__2210.09123__Fourier.tex__415.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 189 *)
s[i_] := (4 i^2)/(4 i^2 - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__189__2210.10781__JMLR-2022.tex__3001.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 190 *)
s[n_] := 41 Binomial[2 n, n] / ((2 n + 1)^4 * 16^n) + 9 Binomial[2 n, n] HarmonicNumber[2 n] / ((2 n + 1)^3 * 16^n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__190__2210.14704__CGLXZ_20221015.tex__686.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 191 *)
s[k_] := (6 k + 1) * (1/2)^3 / (Factorial[k]^3 * 4^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__191__2211.11484__On_two_conjectural_series.tex__99.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 192 *)
s[k_] := (42 k + 5) * (1/2)^3 / (Factorial[k]^3 * 64^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__192__2211.11484__On_two_conjectural_series.tex__105.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 193 *)
s[k_] := Factorial[k] / Factorial[2 k + 1];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__193__2211.11484__On_two_conjectural_series.tex__116.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 194 *)
s[k_] := (6*k + 1) * (1/2)^3 * Factorial[k]^-3 * 4^-k * Sum[1/(2*j - 1)^2 - 1/(16*j^2), {j, 1, k}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__194__2211.11484__On_two_conjectural_series.tex__128.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 195 *)
s[k_] := (6 k + 1) * ((1/2)^k)^3 / (Factorial[k]^3 * 4^k) * (Harmonic[2 k, 2] - 5/16 * Harmonic[k, 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__195__2211.11484__On_two_conjectural_series.tex__166.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 196 *)
s[k_] := (42 k + 5) * (1/2)^3 * Pochhammer[1/2, k]^3 / (Factorial[k]^3 * 64^k) * (Harmonic[2 k, 2] - 25/92 * Harmonic[k, 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__196__2211.11484__On_two_conjectural_series.tex__187.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 197 *)
s[k_] := ((1/2)^k)^3 / (Factorial[k]^3 * 64^k) * ((42*k + 5) * (2*HarmonicNumber[k, 2] - 7*HarmonicNumber[2*k, 2]) + 9/(1 + 2*k));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__197__2211.11484__On_two_conjectural_series.tex__522.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 198 *)
s[k_] := ((1/2)^k)^3 / (Factorial[k]^3 * 64^k) * ((42*k + 5) * (4*HarmonicNumber[2*k, 2] - HarmonicNumber[k, 2]) + 8/(1 + 2*k));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__198__2211.11484__On_two_conjectural_series.tex__552.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 199 *)
s[n_] := 4^(-n) * Factorial[n] / Pochhammer[1/2, n] * (-HarmonicNumber[n]/n^3 + 3*HarmonicNumber[n]^2/(2*n^2) - 3*HarmonicNumber[n, 2]/(2*n^2) + 3/n^4);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__199__2212.02986__article.tex__297.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 200 *)
s[n_] := (-1/4)^n * Pochhammer[1/2, n] / Pochhammer[1, n] * (1 / (2*n + 1)^2) * (5*HarmonicNumber[2*n + 1] + 12/(2*n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__200__2212.02986__article.tex__380.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 201 *)
s[k_] := 4^(-3 k) * Factorial[k - 1]^3 / Factorial[k - 1/2]^3 * (21/k^2 - 8/k^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__201__2212.02986__article.tex__401.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 202 *)
s[k_] := 2^(-10 k) * Factorial[k]^5 / (k^5 * Factorial[1/2 + k - 1]^5) * (205 k^2 - 160 k + 32);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__202__2212.02986__article.tex__422.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 203 *)
s[n_] := 1/(n^2 Binomial[2 n, n]) * (12 Sum[(-1)^j / j^2, {j, 1, n}] - (-1)^n / n^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__203__2212.02986__article.tex__453.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 204 *)
s[n_] := Binomial[2 n, n] / ((2 n + 1) * 16^n) * (12 * Sum[(-1)^j / (2 j + 1)^2, {j, 0, n}] - (-1)^n / (2 n + 1)^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__204__2212.02986__article.tex__477.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 205 *)
s[n_] := (2^(-8))^n * Binomial[2*n, n]^3 * n^2 / ((2*n - 1)*(2*n - 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__205__2212.09965__AccelerationV30.tex__337.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 206 *)
s[n_] := -2 * (2^(-4))^n * Binomial[2*n, n] * (6*n + 5) / ((2*n + 3) * (2*n + 1) * (2*n - 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__206__2212.09965__AccelerationV30.tex__337.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 207 *)
s[k_] := 2^(4 k) / ((2 k + 1) k (k - 1) Binomial[2 k, k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__207__2212.09965__AccelerationV30.tex__337.json",
	2,
	200,
	"series"
];

ClearAll[n];

(* 208 *)
s[n_] := -1/8 * (2^(-12))^n * Binomial[2*n, n]^3 * (6*n + 1) * (14*n - 3) * (2*n + 1) / (2*n - 1)^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__208__2212.09965__AccelerationV30.tex__349.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 209 *)
s[k_] := 2^(4 k) * (14 k^2 + 11 k + 1) * (k + 1) / (k * (4 k + 3) * (4 k + 1)^2 * (2 k - 1) * Binomial[2 k, k] * Binomial[4 k, 2 k]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__209__2212.09965__AccelerationV30.tex__349.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 210 *)
s[k_] := (14 k + 11) (2 k + 1) (3 k + 1) Binomial[2 k, k] / ((4 k + 3) (4 k + 1)^2 (2 k - 1) Binomial[4 k, 2 k]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__210__2212.09965__AccelerationV30.tex__349.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 211 *)
s[j_] := (-2^4)^j * (40*j^2 - 12*j - 1) * Binomial[2*j, j] / (j * (2*j - 1)^2 * (4*j + 1) * Binomial[4*j, 2*j]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__211__2212.09965__AccelerationV30.tex__426.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 212 *)
s[k_] := (((1/2)^5 * (1/3) * (2/3) * (1/4) * (3/4))^n / (1^9) * (4528 k^4 + 3180 k^3 + 972 k^2 + 147 k + 9) * (-27/256)^n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__212__2212.09965__AccelerationV30.tex__674.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 213 *)
s[n_] := (-1/64)^n * Binomial[2*n, n]^3 * (4*n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__213__2212.13305__ComplexV8.tex__69.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 214 *)
s[k_] := (-1)^k / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__214__2212.13687__XZZ0701.tex__568.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 215 *)
s[k_] := Sech[Pi k];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__215__2301.03738__JacobiV5.tex__670.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 216 *)
s[k_] := (6 k + 1) * (1/2)^3 / (Factorial[k]^3 * 4^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__216__2301.12932__SOME_DOUBLE_SERIES_FOR____AND_THEIR_q-ANALOGUES.tex__77.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 217 *)
s[k_] := (-1)^k * (4*k + 1) * (1/2)^(k^3) / (Factorial[k]^3) * Sum[(-1)^i / i^2, {i, 1, 2*k}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__217__2301.12932__SOME_DOUBLE_SERIES_FOR____AND_THEIR_q-ANALOGUES.tex__108.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 218 *)
s[n_] := 1/16^n * (4/(8*n + 1) - 2/(8*n + 4) - 1/(8*n + 5) - 1/(8*n + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__218__2302.06640__Batir-BMMSS-R2.tex__78.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 219 *)
s[n_] := Binomial[2 n, n] * (HarmonicNumber[2 n] - HarmonicNumber[n]) / 8^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__219__2302.06640__Batir-BMMSS-R2.tex__758.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 220 *)
s[k_] := (1 + 6 k) / (4^k) * (1/2)^k^3 / (1)^k^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__220__2303.05402__On_a_conjectural_series_3.tex__107.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 221 *)
s[k_] := (1 + 6 k)/4^k * (1/2)^k^3 / (1)^k^3 * Sum[1/(2 j - 1)^2 - 1/(16 j^2), {j, 1, k}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__221__2303.05402__On_a_conjectural_series_3.tex__144.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 222 *)
s[k_] := (1 + 6 k)/4^k * (1/2)^3 * 1^3 * (HarmonicNumber[2 k, 2] - (5/16) * HarmonicNumber[k, 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__222__2303.05402__On_a_conjectural_series_3.tex__162.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 223 *)
s[k_] := (1/32)^k * Binomial[2*k, k]^2 * Harmonic[2*k]/(2*k - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__223__2304.00360__HalfV26.tex__131.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 224 *)
s[n_] := (1/2) * (1/4)^n * Binomial[2*n, n] / (4*n + 1)^2 + (9/8) * (1/4)^n * Binomial[2*n, n] / (4*n - 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__224__2304.00360__HalfV26.tex__669.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 225 *)
s[n_] := 9/8 * (1/4)^n * Binomial[2*n, n] / (4*n - 3) - 3/4 * (1/4)^n * Binomial[2*n, n] / (4*n - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__225__2304.00360__HalfV26.tex__688.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 226 *)
s[k_] := (1/4)^k * Binomial[2*k, k] * 1/(4*k - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__226__2304.00360__HalfV26.tex__704.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 227 *)
s[n_] := (1/2) * (1/4)^n * Binomial[2*n, n] / (4*n + 1)^2 + (9/8) * (1/4)^n * Binomial[2*n, n] / (4*n - 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__227__2304.00360__HalfV26.tex__704.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 228 *)
s[n_] := (9/8) * (1/4)^n * Binomial[2*n, n] / (4*n - 3) - (3/4) * (1/4)^n * Binomial[2*n, n] / (4*n - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__228__2304.00360__HalfV26.tex__722.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 229 *)
s[n_] := (1/4)^n * Binomial[2 n, n] * (9/(8 (4 n - 3)) - 3/(4 (4 n - 1)));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__229__2304.00360__HalfV26.tex__737.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 230 *)
s[n_] := (9/8) * (1/4)^n * Binomial[2*n, n] / (4*n - 3) - (3/4) * (1/4)^n * Binomial[2*n, n] / (4*n - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__230__2304.00360__HalfV26.tex__752.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 231 *)
s[n_] := (1/4)^n * Binomial[2*n, n] * (3/16 * 1/(n + 1) + 3/8 * 1/(4*n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__231__2304.00360__HalfV26.tex__759.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 232 *)
s[n_] := (1/4)^n * Binomial[2*n, n] / (4*n + 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__232__2304.00360__HalfV26.tex__759.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 233 *)
s[k_] := 1/(2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__233__2304.03684__calculus-india-vsingh-for-arxiv-010423.tex__308.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 234 *)
s[k_] := 1/4^k * (1/2)^k^3 / (1)^k^3 * (6 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__234__2305.00498__Sun-conjecture-230628.tex__88.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 235 *)
s[k_] := (-1)^k * (1/2)^3 * (4*k + 1) / (1)^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__235__2305.00498__Sun-conjecture-230628.tex__88.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 236 *)
s[k_] := 1/64^k * (1/2)^k^3 / (1)^k^3 * (42*k + 5);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__236__2305.00498__Sun-conjecture-230628.tex__88.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 237 *)
s[k_] := Pochhammer[1/2, k] * Pochhammer[1/4, k] * Pochhammer[3/4, k] / ((-4)^k * Pochhammer[1, k]^3) * (20 k + 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__237__2305.00498__Sun-conjecture-230628.tex__88.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 238 *)
s[k_] := 1/4^k * (1/2)^k^3 / (1)^k^3 * ((6 k + 1) HarmonicNumber[k] - 2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__238__2305.00498__Sun-conjecture-230628.tex__133.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 239 *)
s[k_] := 1/4^k * (1/2)^k^3 / (1)^k^3 * ((6*k + 1) * HarmonicNumber[2*k] - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__239__2305.00498__Sun-conjecture-230628.tex__139.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 240 *)
s[k_] := 1/4^k * (1/2)^3 * (6*k + 1) * (-2*HarmonicNumber[2*k, 2] + HarmonicNumber[k, 2] + 6*(HarmonicNumber[2*k] - HarmonicNumber[k])^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__240__2305.00498__Sun-conjecture-230628.tex__145.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 241 *)
s[k_] := 1/4^k * (1/2)^k^3 / 1^k^3 * ((6*k + 1) * (HarmonicNumber[2*k] - HarmonicNumber[k]) + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__241__2305.00498__Sun-conjecture-230628.tex__175.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 242 *)
s[k_] := Pochhammer[1/2, k] * Pochhammer[1/4, k] * Pochhammer[3/4, k] / ((-4)^k * Pochhammer[1, k]^3) * ((20*k + 3) * (2*HarmonicNumber[k, -3/4] - HarmonicNumber[k, -1/4] + HarmonicNumber[k] - 4) + 8);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__242__2305.00498__Sun-conjecture-230628.tex__393.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 243 *)
s[k_] := (Pochhammer[1/2, k] * Pochhammer[1/4, k] * Pochhammer[3/4, k]) / ((-4)^k * Pochhammer[1, k]^3) * ((20*k + 3) * (2*HarmonicNumber[k, -1/4] - HarmonicNumber[k, -3/4] + HarmonicNumber[k]) - 12);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__243__2305.00498__Sun-conjecture-230628.tex__413.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 244 *)
s[k_] := (20 k + 3) * rf[1/2, k] * rf[1/4, k] * rf[3/4, k] / ((-4)^k * Factorial[k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__244__2305.00498__Sun-conjecture-230628.tex__418.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 245 *)
s[k_] := (4 k^2)/(4 k^2 - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__245__2305.02989__GH.tex__167.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 246 *)
s[i_] := 1/16^i * (4/(8*i + 1) - 2/(8*i + 4) - 1/(8*i + 5) - 1/(8*i + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__246__2305.04935__main.tex__778.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 247 *)
s[k_] := (-1)^k / ((2*k - 1) * (2*k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__247__2305.14367__KA_RF_A-series-of-Ramanujan-two-term-dilogarithm-identities_20230529.tex__566.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 248 *)
s[p_] := (-1)^p / (p + 1/2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__248__2305.14995__Manuscript_VArxiv24.tex__2897.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 249 *)
s[k_] := (HarmonicNumber[3 k] - 8 HarmonicNumber[2 k] + 7 HarmonicNumber[k]) / (2^k * Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__249__2306.04638__sigma23-074.tex__212.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 250 *)
s[j_] := 1/(j^2 (2 j + 1)) * Factorial[j]^2 / Factorial[2 j - 1] * Binomial[2 j - 2, j - 1];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__250__2306.15727__Areal_Mahler_Measure_Lalin_Roy.tex__682.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 251 *)
s[k_] := (27/4)^k / (k^2 Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__251__2306.16889__KA_RF_TG_On_some_series_involving_the_binomial_coefficients_20230721.tex__115.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 252 *)
s[k_] := (8/3)^k / (k^2 Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__252__2306.16889__KA_RF_TG_On_some_series_involving_the_binomial_coefficients_20230721.tex__124.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 253 *)
s[k_] := (8/3)^k / (k * Binomial[3*k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__253__2306.16889__KA_RF_TG_On_some_series_involving_the_binomial_coefficients_20230721.tex__170.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 254 *)
s[k_] := (25 k - 3) / (2^k * Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__254__2307.03086__P85i.tex__148.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 255 *)
s[k_] := 1 / ((2*k - 1) * 2^k * Binomial[3*k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__255__2307.03086__P85i.tex__208.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 256 *)
s[k_] := 8^k / ((2*k - 1) * 3^k * Binomial[3*k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__256__2307.03086__P85i.tex__216.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 257 *)
s[k_] := (HarmonicNumber[3 k] - HarmonicNumber[k]) / ((2 k - 1) * 2^k * Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__257__2307.03086__P85i.tex__264.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 258 *)
s[k_] := (30 k - 11) / ((2 k - 1) Binomial[4 k, 2 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__258__2307.03086__P85i.tex__355.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 259 *)
s[k_] := (42 k + 5) * Binomial[2 k, k]^3 / 4096^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__259__2307.03086__P85i.tex__448.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 260 *)
s[k_] := (42 k + 5) * Binomial[2 k, k]^3 / 4096^k * (Harmonic[2 k, 2] - 25/92 * Harmonic[k, 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__260__2307.03086__P85i.tex__460.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 261 *)
s[k_] := Binomial[2 k, k]^3 / 4096^k * ((42 k + 5) * (7 HarmonicNumber[2 k, 2] - 2 HarmonicNumber[k, 2]) - 9/(2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__261__2307.03086__P85i.tex__464.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 262 *)
s[k_] := Binomial[2 k, k]^3 / 4096^k * ((42 k + 5) * (4 HarmonicNumber[2 k, 2] - HarmonicNumber[k, 2]) + 8/(2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__262__2307.03086__P85i.tex__466.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 263 *)
s[k_] := Binomial[2 k, k]^3 / 4096^k * ((42 k + 5) * HarmonicNumber[k, 2] + 92 / (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__263__2307.03086__P85i.tex__468.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 264 *)
s[k_] := Binomial[2 k, k]^3 / 256^k * ((6 k + 1) HarmonicNumber[k]^2 + 8 / (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__264__2307.03086__P85i.tex__488.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 265 *)
s[k_] := 8^k / ((k + 1) * 3^k * Binomial[3*k, k]) - 3 * 8^k / ((3*k + 1) * 3^k * Binomial[3*k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__265__2307.03086__P85i.tex__693.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 266 *)
s[k_] := (HarmonicNumber[2 k] - HarmonicNumber[k]) / ((3 k + 1) * 2^k * Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__266__2307.03086__P85i.tex__737.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 267 *)
s[k_] := (HarmonicNumber[k] - HarmonicNumber[3*k + 1]) / ((3*k + 1)*(2*k - 1)*2^k*Binomial[3*k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__267__2307.03086__P85i.tex__752.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 268 *)
s[k_] := (-1)^k * ((28*k^2 - 41*k + 9) * (2*HarmonicNumber[2*k - 1] + 5*HarmonicNumber[k - 1]) - 21*k + 3) / ((2*k - 1) * k * Binomial[2*k, k] * Binomial[3*k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__268__2307.03086__P85i.tex__1099.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 269 *)
s[k_] := (-1)^k * (6 * (28*k^2 - 41*k + 9) * (HarmonicNumber[3*k - 1] - 6*HarmonicNumber[k - 1]) - 142*k + 125) / ((2*k - 1) * k * Binomial[2*k, k] * Binomial[3*k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__269__2307.03086__P85i.tex__1103.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 270 *)
s[k_] := ((-1)^k * (12 * (21*k^2 - 23*k + 4) * (2*HarmonicNumber[2*k - 1] + 5*HarmonicNumber[k - 1]) + 35*k - 121)) / ((2*k - 1) * Binomial[2*k, k] * Binomial[3*k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__270__2307.03086__P85i.tex__1115.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 271 *)
s[k_] := ((-1)^k * (108 * (21*k^2 - 23*k + 4) * (HarmonicNumber[3*k - 1] - 6*HarmonicNumber[k - 1]) - 3247*k + 2537)) / ((2*k - 1) * Binomial[2*k, k] * Binomial[3*k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__271__2307.03086__P85i.tex__1119.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 272 *)
s[k_] := (-16)^k * ((40*k^2 - 52*k + 7) * (3*HarmonicNumber[2*k - 1] + 2*HarmonicNumber[k - 1]) - 20*k - 11) / ((2*k - 1) * k * Binomial[2*k, k] * Binomial[4*k, 2*k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__272__2307.03086__P85i.tex__1257.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 273 *)
s[k_] := (-16)^k * ((40*k^2 - 52*k + 7) * (9*HarmonicNumber[4*k - 1] - 3*HarmonicNumber[2*k - 1] - 17*HarmonicNumber[k - 1]) - 298*k + 233) / ((2*k - 1) * k * Binomial[2*k, k] * Binomial[4*k, 2*k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__273__2307.03086__P85i.tex__1261.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 274 *)
s[k_] := (-16)^k * (7 * (140*k^2 - 94*k - 15) * (3*HarmonicNumber[2*k - 1] + 2*HarmonicNumber[k - 1]) + 15 * (226*k - 249)) / ((2*k - 1) * Binomial[2*k, k] * Binomial[4*k, 2*k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__274__2307.03086__P85i.tex__1273.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 275 *)
s[k_] := (-16)^k * (7 * (140*k^2 - 94*k - 15) * (2*HarmonicNumber[4*k - 1] + 5*HarmonicNumber[2*k - 1]) + 48 * (19*k - 45)) / ((2*k - 1) * Binomial[2*k, k] * Binomial[4*k, 2*k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__275__2307.03086__P85i.tex__1277.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 276 *)
s[k_] := (-16)^k * ((20 k^2 - 8 k + 1) * HarmonicNumber[2 k - 1, 2] - 3 k (4 k - 1) / (2 k - 1)^2) / ((2 k - 1)^2 * k^3 * Binomial[2 k, k] * Binomial[4 k, 2 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__276__2307.03086__P85i.tex__1294.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 277 *)
s[k_] := 256^k * (24 * (1408*k^2 - 6318*k + 3557) * HarmonicNumber[k] + 145906*k + 533701) / ((2*k - 1) * Binomial[3*k, k] * Binomial[6*k, 3*k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__277__2307.03086__P85i.tex__1407.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 278 *)
s[k_] := (-4)^k * Binomial[2*k, k] * ((7*k - 1) * Harmonic[k - 1] - (6*k - 1) / (4*k - 2)) / (k * (2*k - 1) * Binomial[3*k, k] * Binomial[6*k, 3*k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__278__2307.03086__P85i.tex__1440.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 279 *)
s[k_] := (-4)^k * Binomial[2*k, k] / (k * (2*k - 1) * Binomial[3*k, k] * Binomial[6*k, 3*k]) * ((7*k - 1) * (2*HarmonicNumber[6*k - 1] - HarmonicNumber[3*k - 1]) - (34*k - 9)/(4*k - 2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__279__2307.03086__P85i.tex__1446.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 280 *)
s[k_] := ((7 k - 1) * (-4)^k * Binomial[2 k, k]) / ((2 k - 1) * k * Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__280__2307.03086__P85i.tex__1474.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 281 *)
s[k_] := (-4)^k * Binomial[2*k, k] * ((7*k - 1) * (16*Harmonic[6*k - 1] - 8*Harmonic[3*k - 1] - 6*Harmonic[2*k - 1] - 5*Harmonic[k - 1]) - 20) / ((2*k - 1) * k * Binomial[3*k, k] * Binomial[6*k, 3*k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__281__2307.03086__P85i.tex__1481.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 282 *)
s[k_] := (-4)^k * Binomial[2*k, k] * ((7*k - 1) * (8*Harmonic[2*k - 1, 3] - Harmonic[k - 1, 3]) - 12 * (6*k - 1) / (2*k - 1)^3) / ((2*k - 1) * k * Binomial[3*k, k] * Binomial[6*k, 3*k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__282__2307.03086__P85i.tex__1492.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 283 *)
s[k_] := (280 k - 51) (-4)^k Binomial[2 k, k] / (k Binomial[3 k, k] Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__283__2307.03086__P85i.tex__1526.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 284 *)
s[k_] := (952 k - 201) (-4)^k Binomial[2 k, k] / (Binomial[3 k, k] Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__284__2307.03086__P85i.tex__1530.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 285 *)
s[k_] := (8^k * Binomial[2*k, k] / (Binomial[3*k, k] * Binomial[6*k, 3*k])) * (21 * (350*k - 17) * (2 * HarmonicNumber[6*k - 1] - HarmonicNumber[3*k - 1] - HarmonicNumber[k - 1]) + 4850);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__285__2307.03086__P85i.tex__1541.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 286 *)
s[k_] := (8^k * Binomial[2*k, k] / (Binomial[3*k, k] * Binomial[6*k, 3*k])) * (7 * (350*k - 17) * (HarmonicNumber[2*k - 1] - HarmonicNumber[k - 1]) + 2225);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__286__2307.03086__P85i.tex__1547.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 287 *)
s[k_] := Binomial[2 k, k] * 8^k * ((5 k - 1) * (HarmonicNumber[2 k - 1] - HarmonicNumber[k - 1]) - 3 * (6 k - 1)/(8 k - 4))/((2 k - 1) * k * Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__287__2307.03086__P85i.tex__1577.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 288 *)
s[k_] := Binomial[2 k, k] * 8^k * ((5 k - 1) * (2 HarmonicNumber[6 k - 1] - HarmonicNumber[3 k - 1] - HarmonicNumber[k - 1]) - (6 k - 2)/(2 k - 1))/((2 k - 1) k * Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__288__2307.03086__P85i.tex__1581.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 289 *)
s[k_] := Binomial[2 k, k] * 8^k * ((5 k - 1) * (12 HarmonicNumber[6 k - 1] - 6 HarmonicNumber[3 k - 1] - 4 HarmonicNumber[2 k - 1] - 2 HarmonicNumber[k - 1]) - 9) / ((2 k - 1) k Binomial[3 k, k] Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__289__2307.03086__P85i.tex__1586.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 290 *)
s[k_] := Binomial[2 k, k] * ((130 k - 21) * (2 HarmonicNumber[6 k - 1] - HarmonicNumber[3 k - 1] - HarmonicNumber[k - 1]) - 16 * (13 k - 4) / (2 k - 1)) / (k * (2 k - 1) * (-3)^k * Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__290__2307.03086__P85i.tex__1616.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 291 *)
s[k_] := Binomial[2 k, k] * ((130 k - 21) * (26 HarmonicNumber[6 k - 1] - 13 HarmonicNumber[3 k - 1] - 10 HarmonicNumber[2 k - 1] - 3 HarmonicNumber[k - 1]) - 572) / (k * (2 k - 1) * (-3)^k * Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__291__2307.03086__P85i.tex__1622.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 292 *)
s[k_] := Binomial[2 k, k] * (-27)^k * ((10 k - 1) * (6 HarmonicNumber[6 k - 1] - 3 HarmonicNumber[3 k - 1] + 11 HarmonicNumber[k - 1]) - 12) / (k * (2 k - 1) * Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__292__2307.03086__P85i.tex__1647.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 293 *)
s[k_] := Binomial[2 k, k]^2 * Binomial[4 k, 2 k] / (-1024)^k * ((20 k + 3) * (Harmonic[4 k, 2] - Harmonic[2 k, 2]/4 - Harmonic[k, 2]/16) + 1/(4 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__293__2307.03086__P85i.tex__2063.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 294 *)
s[k_] := (20 k + 3) * Binomial[2 k, k]^2 * Binomial[4 k, 2 k] / (-1024)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__294__2307.03086__P85i.tex__2075.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 295 *)
s[k_] := (28 k^2 + 10 k + 1) * Binomial[2 k, k]^5 / ((6 k + 1) * (-64)^k * Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__295__2307.03086__P85i.tex__2122.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 296 *)
s[k_] := (((28 k^2 + 10 k + 1) (10 HarmonicNumber[2 k, 2] - 3 HarmonicNumber[k, 2]) + 2) Binomial[2 k, k]^5) / ((6 k + 1) (-64)^k Binomial[3 k, k] Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__296__2307.03086__P85i.tex__2145.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 297 *)
s[k_] := Binomial[2 k, k]^5 / (-2^20)^k * ((820 k^2 + 180 k + 13) * (351 HarmonicNumber[2 k, 5] - 11 HarmonicNumber[k, 5]) + 275 / (2 k + 1)^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__297__2307.03086__P85i.tex__2213.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 298 *)
s[k_] := Binomial[2 k, k]^7 / 2^(20 k) * ((168 k^3 + 76 k^2 + 14 k + 1) * (128 Harmonic[2 k, 4] - 7 Harmonic[k, 4]) + 64/(2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__298__2307.03086__P85i.tex__2272.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 299 *)
s[k_] := Binomial[2 k, k]^7 / 2^(20 k) * ((168 k^3 + 76 k^2 + 14 k + 1) * (16 HarmonicNumber[2 k, 2] - 5 HarmonicNumber[k, 2]) + 8 (6 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__299__2307.03086__P85i.tex__2285.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 300 *)
s[k_] := Exp[2 Pi k] / (Exp[2 Pi k] - 1)^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__300__2307.03350__RYJCP_Arxiv_1st_version.tex__2729.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 301 *)
s[n_] := (-1)^(n - 1) / (2 n - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__301__2307.05607__chapter6.tex__1276.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 302 *)
s[m_] := (-1)^m / (2 m + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__302__2307.08063__zeta-beta-and-beyond-arxiv.tex__654.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 303 *)
s[k_] := (-1)^k * (4*k + 1) * (1/2)^(k^3) / (1)^(k^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__303__2308.06440__Harmonic_numbers_8.tex__131.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 304 *)
s[k_] := (-1)^(k - 1)/(2 k - 1)^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__304__2308.06440__Harmonic_numbers_8.tex__241.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 305 *)
s[k_] := (22 k^2 - 17 k + 3) * 16^k * Binomial[4 k, 2 k] / (k * (4 k - 1) * (4 k - 3) * Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__305__2310.03699__Hou_Sun.tex__383.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 306 *)
s[k_] := (60 k^2 - 43 k + 8) * Binomial[4 k, 2 k] / (k^3 * (4 k - 1) * Binomial[2 k, k]^4);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__306__2310.03699__Hou_Sun.tex__412.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 307 *)
s[k_] := (1/64)^k * (1/2)^3 * (42*k + 5) / (1)^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__307__2310.04642__Harmonic_numbers_9.tex__161.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 308 *)
s[n_] := ((-1)^n * (1/2)^3 * (1/2 + 2 n)) / (1^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__308__2310.05112__Level3V215.tex__131.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 309 *)
s[k_] := (6 k + 1) * (1/2)^3 / (Factorial[k]^3 * 4^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_200000-349999/recurrence__309__2310.15207__qLucas.tex__63.json",
	0,
	200,
	"series"
];

ClearAll[n];




(* ::Text:: *)
(*math.CA_0-22736*)


(*
(* 0 *)
s[k_] := Binomial[2 k, k] / (2^(2 k) * (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__0__0705.2379__part5.tex__662.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 1 *)
s[k_] := 2^k / (k * Binomial[2 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__1__0707.2124__part9.tex__1008.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 2 *)
s[k_] := (-1)^k / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__2__0707.2500__pgis13.tex__1849.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 3 *)
s[n_] := ((-1)^n * (1/2)^(n^3)) / (Factorial[n]^3) * (4*n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__3__0712.1332__rampery2e-xxx.tex__131.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 4 *)
s[n_] := ((1/4)^n * (1/2)^n * (3/4)^n / (Factorial[n]^3)) * (21460 n + 1123) * ((-1)^n) / (882^(2 n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__4__0712.1332__rampery2e-xxx.tex__138.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 5 *)
s[n_] := (Pochhammer[1/4, n] * Pochhammer[1/2, n] * Pochhammer[3/4, n]) / (Factorial[n]^3) * (26390 n + 1103) * 1/(99^(4 n + 2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__5__0712.1332__rampery2e-xxx.tex__138.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 6 *)
s[n_] := (Pochhammer[1/3, n] * Pochhammer[1/2, n] * Pochhammer[2/3, n] / Factorial[n]^3) * (14151 n + 827) * ((-1)^n / 500^(2 n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__6__0712.1332__rampery2e-xxx.tex__176.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 7 *)
s[n_] := ((1/2)^n)^5 / (Factorial[n]^5) * (20 n^2 + 8 n + 1) * ((-1)^n) / (2^(2 n));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__7__0712.1332__rampery2e-xxx.tex__441.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 8 *)
s[n_] := (Pochhammer[1/2, n] * Pochhammer[1/4, n] * Pochhammer[3/4, n] * Pochhammer[1/6, n] * Pochhammer[5/6, n] / Factorial[n]^5) * (1640 n^2 + 278 n + 15) * (-1)^n / 2^(10 n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__8__0712.1332__rampery2e-xxx.tex__455.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 9 *)
s[n_] := Pochhammer[1/2, n] * Pochhammer[1/4, n] * Pochhammer[3/4, n] / (Factorial[n]^3) * (28 n + 3) * (-1)^n / 48^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__9__0712.1332__rampery2e-xxx.tex__474.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 10 *)
s[n_] := (Pochhammer[1/2, n]^3 / Factorial[n]^3) * (6 n + 1) * (-1)^n / 8^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__10__0805.2788__exp01n.tex__74.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 11 *)
s[n_] := Pochhammer[1/2, n]^3 / Factorial[n]^3 * (4 n + 1) * (-1)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__11__0805.2788__exp01n.tex__74.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 12 *)
s[n_] := (1/2)^n^3 / Factorial[n]^3 * (6 n + 1) / 4^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__12__0805.2788__exp01n.tex__74.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 13 *)
s[n_] := (1/2)^n * (1/4)^n * (3/4)^n / (Factorial[n]^3) * (20 n + 3) * (-1)^n / 2^(2 n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__13__0805.2788__exp01n.tex__149.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 14 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__14__0806.0150__Fourier.tex__273.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 15 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__15__0806.0150__Fourier.tex__395.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 16 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__16__0806.0150__Fourier.tex__1518.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 17 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__17__0806.0150__Fourier.tex__1528.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 18 *)
s[k_] := (2 k) (2 k) / ((2 k - 1) (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__18__1004.2453__ws.tex__84.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 19 *)
s[k_] := Binomial[2 k, k] * 2^(-2 k) / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__19__1004.2453__ws.tex__232.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 20 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__20__1004.4712__bulloughproc.tex__286.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 21 *)
s[k_] := (-1)^k / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__21__1010.4298__165s.tex__212.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 22 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1) * 8^k) * (Sum[(-1)^j / (2 j + 1), {j, 0, k - 1}] - (-1)^k / (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__22__1010.4298__165s.tex__722.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 23 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1)^2 * (-16)^k) * (40 Sum[(-1)^j / (2 j + 1)^3, {j, 0, k - 1}] - 7 * (-1)^k / (2 k + 1)^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__23__1010.4298__165s.tex__727.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 24 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1) * 16^k) * (8 * Sum[(-1)^j / (2 j + 1)^4, {j, 0, k}] + (-1)^k / (2 k + 1)^4);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__24__1010.4298__165s.tex__750.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 25 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1)^2 * (-16)^k) * (110 * Sum[(-1)^j / (2 j + 1)^4, {j, 0, k}] + 29 * (-1)^k / (2 k + 1)^4);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__25__1010.4298__165s.tex__758.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 26 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1)^3 * 16^k) * (72 * Sum[(-1)^j / (2 j + 1)^2, {j, 0, k}] - (-1)^k / (2 k + 1)^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__26__1010.4298__165s.tex__762.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 27 *)
s[k_] := (4 k + 1) * Binomial[2 k, k]^3 / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__27__1101.0600__151n.tex__200.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 28 *)
s[k_] := (25 k - 3) / (2^k * Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__28__1101.0600__151n.tex__228.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 29 *)
s[k_] := (30 k + 7) / ((-256)^k * Binomial[2 k, k]^2 * T_k[1, 16]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__29__1101.0600__151n.tex__766.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 30 *)
s[k_] := (30 k + 7) / ((-256)^k * Binomial[2 k, k]^2 * T_k[1, 16]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__30__1101.0600__151n.tex__1464.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 31 *)
s[k_] := (15 k + 2) Binomial[2 k, k] Binomial[3 k, k] T_k[18, 6]/972^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__31__1101.0600__151n.tex__1484.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 32 *)
s[k_] := (13940 k + 1559) / ((-5760^2)^k * Binomial[2 k, k]^2 * T2k[322, 1]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__32__1101.0600__151n.tex__1558.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 33 *)
s[k_] := (340 k + 59) / ((-480^2)^k * Binomial[2 k, k]^2 * T2k[62, 1]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__33__1101.0600__151n.tex__1558.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 34 *)
s[k_] := (26 k + 5) / ((-48^2)^k * Binomial[2 k, k]^2 * T[2 k, 7, 1]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__34__1101.0600__151n.tex__1558.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 35 *)
s[k_] := 2^k / (k^2 * Binomial[2 k, k]) * (Harmonic[Floor[k/2]] - (-1)^k * 2/k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__35__1102.5649__ConjSeries.tex__140.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 36 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1) * 16^k) * (3 HarmonicNumber[2 k + 1] + 4 / (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__36__1102.5649__ConjSeries.tex__167.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 37 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1)^2 * (-16)^k) * (5 HarmonicNumber[2 k + 1] + 12 / (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__37__1102.5649__ConjSeries.tex__167.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 38 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1) * 8^k) * (Sum[(-1)^j / (2 j + 1), {j, 0, k}] - 2 * (-1)^k / (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__38__1102.5649__ConjSeries.tex__202.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 39 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1)^3 * 16^k) * (72 * Sum[(-1)^j / (2 j + 1)^2, {j, 0, k}] - (-1)^k / (2 k + 1)^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__39__1102.5649__ConjSeries.tex__211.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 40 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1)^2 * (-16)^k) * (110 * Sum[(-1)^j / (2 j + 1)^4, {j, 0, k}] + 29 * (-1)^k / (2 k + 1)^4);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__40__1102.5649__ConjSeries.tex__211.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 41 *)
s[k_] := (8 k + 1) / ((-4032)^k * Binomial[2 k, k] * S[4, k, 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__41__1102.5649__ConjSeries.tex__317.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 42 *)
s[n_] := (21 n + 1)/64^n * Sum[Binomial[n, k] * Binomial[2 k, n] * Binomial[2 k, k] * Binomial[2 n - 2 k, n - k] * 3^(2 k - n), {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__42__1102.5649__ConjSeries.tex__372.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 43 *)
s[n_] := n/4^n * Sum[Binomial[-1/4, k]^2 * Binomial[-3/4, n - k]^2, {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__43__1102.5649__ConjSeries.tex__487.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 44 *)
s[n_] := (9 n + 1)/64^n * Sum[Binomial[-1/4, k]^2 * Binomial[-3/4, n - k]^2, {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__44__1102.5649__ConjSeries.tex__487.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 45 *)
s[k_] := (357 k + 103)/2160^k * Binomial[2 k, k] * Sum[Binomial[k, j] * Binomial[k + 2 j, 2 j] * Binomial[2 j, j] * (-324)^(k - j), {j, 0, k}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__45__1102.5649__ConjSeries.tex__523.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 46 *)
s[k_] := (14 k + 3) Binomial[2 k, k] P[k, -7]/8^(2 k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__46__1102.5649__ConjSeries.tex__558.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 47 *)
s[k_] := 2^(-4 k) / (2 k + 1) * Binomial[2 k, k];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__47__1103.3893__logsin.tex__637.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 48 *)
s[k_] := (6 k + 1) / ((-512)^k * Binomial[2 k, k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__48__1104.3856__157b.tex__114.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 49 *)
s[k_] := (65 k + 8) / ((-63^2)^k * Binomial[2 k, k]^2 * Binomial[4 k, 2 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__49__1104.3856__157b.tex__114.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 50 *)
s[k_] := (5 k + 1) / ((-192)^k * Binomial[2 k, k]^2 * Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__50__1104.3856__157b.tex__114.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 51 *)
s[n_] := n/54^n * Sum[Binomial[2*k, k] * Binomial[3*k, k] * Binomial[2*(n - k), n - k] * Binomial[3*(n - k), n - k], {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__51__1104.3856__157b.tex__128.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 52 *)
s[k, n_] := Factorial[2 k]^2 * Factorial[2 n - 2 k]^2 / (Factorial[k]^4 * Factorial[n - k]^4 * 32^n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__52__1104.3856__157b.tex__128.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 53 *)
s[k_] := Factorial[2 k]/(128^k * Factorial[k]^2) * (4/(2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__53__1104.3856__157b.tex__163.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 54 *)
s[n_] := (9 n + 1)/64^n * Sum[Binomial[-1/4, k]^2 * Binomial[-3/4, n - k]^2, {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__54__1104.3856__157b.tex__175.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 55 *)
s[n, k_] := Binomial[-1/4, k]^2 * Binomial[-3/4, n - k]^2 / 4^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__55__1104.3856__157b.tex__175.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 56 *)
s[k_] := Binomial[2 k, k]^2 * Binomial[3 k, k] / (-216)^k * Sum[(9 (k + j) + 2) * Binomial[k, j] * (-27)^j / (-216)^j, {j, 0, k}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__56__1104.3856__157b.tex__280.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 57 *)
s[k_] := Binomial[2 k, k]^2 * Binomial[3 k, k] * (9 k + 2 + k) * (9/8)^k / (-216)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__57__1104.3856__157b.tex__280.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 58 *)
s[k_] := Binomial[2 k, k]^2 * Binomial[3 k, k] / (-216)^k * ((9 k + 2) * Sum[Binomial[k, j] / 8^j, {j, 0, k}] + 9 k / 8 * Sum[Binomial[k - 1, j - 1] / 8^(j - 1), {j, 1, k - 1}]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__58__1104.3856__157b.tex__280.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 59 *)
s[n_] := (9 n + 2) / ((-216)^n) * Sum[Binomial[2 k, k]^2 * Binomial[3 k, k] * Binomial[k, n - k] * (-27)^(n - k), {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__59__1104.3856__157b.tex__280.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 60 *)
s[k_] := (7 k + 1) * Binomial[4 k, 2 k] * Binomial[2 k, k]^2 / 648^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__60__1104.3856__157b.tex__320.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 61 *)
s[n_] := (8 n + 1)/576^n * Sum[Binomial[4 k, 2 k] * Binomial[2 k, k]^2 * Binomial[k, n - k] * (-64)^(n - k), {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__61__1104.3856__157b.tex__320.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 62 *)
s[k_] := Binomial[4 k, 2 k] * Binomial[2 k, k]^2 / 576^k * ((8 k + 1) * Sum[Binomial[k, j] / (-9)^j, {j, 0, k}] - 8 k / 9 * Sum[Binomial[k - 1, j - 1] / (-9)^(j - 1), {j, 1, k}]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__62__1104.3856__157b.tex__320.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 63 *)
s[n_] := (9 n + 1)/64^(2 n) * Sum[Binomial[2 k, k]^3 * Binomial[2 (n - k), n - k] * 16^(n - k), {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__63__1104.3856__157b.tex__369.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 64 *)
s[k_] := Binomial[2 k, k]^3 / 4096^k * Sum[(9 (k + j) + 1) / 256^j * Binomial[2 j, j], {j, 0, Infinity}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__64__1104.3856__157b.tex__369.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 65 *)
s[k_] := (10 k + 1) / ((-1536)^k) * Binomial[2 k, k] * (-32);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__65__1104.3856__157b.tex__403.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 66 *)
s[k_] := (1190 k + 163) / ((-4608)^k * Binomial[2 k, k] * S[k, -64]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__66__1104.3856__157b.tex__431.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 67 *)
s[k_] := (357 k + 103)/2160^k * Binomial[2 k, k] * Sum[Binomial[k, j] * Binomial[k + 2 j, 2 j] * Binomial[2 j, j] * (-324)^(k - j), {j, 0, k}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__67__1104.3856__157b.tex__462.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 68 *)
s[k_] := (30 k + 7) / ((-256)^k) * Binomial[2 k, k]^2 * T_k[1, 16];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__68__1205.5402__legendre.tex__43.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 69 *)
s[k_] := (2 k)^2 / ((2 k - 1) (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__69__1206.1801__zeta.tex__185.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 70 *)
s[k_] := 1 - 1/(4 k^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__70__1209.5739__summClaculus6.tex__1343.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 71 *)
s[k_] := 1/(4 k - 3) - 1/(4 k - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__71__1209.5739__summClaculus6.tex__3001.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 72 *)
s[k_] := ((-1)^k * HypergeometricPFQ[{1/6, 1/2, 5/6}, {}, k] * (13591409 + 545140134*k)) / (Factorial[k]^3 * 53360^(3*k + 2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__72__1210.0269__lost02b.tex__294.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 73 *)
s[n_] := (1/2)^n^3 / Factorial[n]^3 * (1 + 6 n) / 4^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__73__1210.0269__lost02b.tex__294.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 74 *)
s[k_] := Binomial[2 k, k]^3 * (27 - 30*2^(1/3) + 6*2^(2/3) + (66 - 84*2^(1/3) + 12*2^(2/3))*k) / (2*(1 + 2^(1/3) + 2^(2/3)))^(8*k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__74__1211.6563__polytope.tex__1171.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 75 *)
s[k_] := Binomial[2 k, k]^2 * Binomial[3 k, k] * (12 + (68 - 4 I) k) / (-146 + 322 I)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__75__1211.6563__polytope.tex__1288.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 76 *)
s[k_] := (762300 - 300288*2^(1/3) - 223080*2^(2/3) + (721776 - 329760*2^(1/3) - 38880*2^(2/3))*k) / (1170 + 928*2^(1/3) + 736*2^(2/3))^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__76__1211.6563__polytope.tex__4013.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 77 *)
s[k_] := (11305476 + 2838336 * 2^(1/3) - 6752280 * 2^(2/3) + (16802544 + 22575840 * 2^(1/3) - 7185120 * 2^(2/3)) * k) / (-1170 - 928 * 2^(1/3) - 736 * 2^(2/3))^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__77__1211.6563__polytope.tex__4024.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 78 *)
s[k_] := Binomial[2 k, k]^2 * Tn[34] * (23 + 60 k) / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__78__1211.6563__polytope.tex__4693.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 79 *)
s[k_] := Binomial[2 k, k]^2 * Tn[194] * (59 + 140 k) / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__79__1211.6563__polytope.tex__4702.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 80 *)
s[k_] := Binomial[2 k, k]^2 * Tn[898] * (35 + 102 k) / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__80__1211.6563__polytope.tex__4720.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 81 *)
s[k_] := Binomial[2 k, k]^2 * Tn[39202] * (68403 + 149292 k) / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__81__1211.6563__polytope.tex__4729.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 82 *)
s[l_] := (-1)^l / (2 l + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__82__1301.2584__spheres.tex__134.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 83 *)
s[k_] := 2^(4 k + 1) * Factorial[k]^4 * (k + 1) / Factorial2[2 k + 1]^4 * HypergeometricPFQ[{1/2, 1/2, 1/2, 1/2, k + 1, k + 1, (k + 3)/2}, {1, (k + 1)/2, (k + 3)/2, (k + 3)/2, (k + 3)/2, (k + 3)/2}, 1];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__83__1301.2584__spheres.tex__645.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 84 *)
s[k_] := 2^(2 k - 1) * Factorial[k]^2 / (Factorial2[2 k + 1]^2 * k) * HypergeometricPFQ[{1/2, 1/2, k + 1, k + 1}, {1, k + 3/2, k + 3/2}, 1];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__84__1301.2584__spheres.tex__648.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 85 *)
s[m_] := 1/(2 m + 1) * ((2 m - 1)!! / (2^m * Factorial[m]))^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__85__1301.2584__spheres.tex__660.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 86 *)
s[n_] := (1/2)^n^3 / Factorial[n]^3 * (1 + 6 n) / 2^(2 n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__86__1302.0548__transart2013-02-19.tex__91.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 87 *)
s[n_] := Pochhammer[1/2, n] * Pochhammer[1/4, n] * Pochhammer[3/4, n] * (1 + 10 n) / (Factorial[n]^3 * 3^(4 n));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__87__1302.0548__transart2013-02-19.tex__91.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 88 *)
s[k_] := (1/2)^3 * (5 + 42 k) / (Factorial[k]^3 * 2^(6 k));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__88__1302.0548__transart2013-02-19.tex__91.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 89 *)
s[n_] := Pochhammer[1/2, n] * Pochhammer[1/4, n] * Pochhammer[3/4, n] / (Factorial[n]^3) * (-1/48)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__89__1302.0548__transart2013-02-19.tex__373.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 90 *)
s[n_] := Sum[Binomial[n, j]^4 * (1 + 3 n) * (-1/20)^n, {j, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__90__1302.0548__transart2013-02-19.tex__435.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 91 *)
s[n_] := Binomial[n, j]^4 * (-1/20)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__91__1302.0548__transart2013-02-19.tex__441.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 92 *)
s[n_] := Pochhammer[1/2, n] * Pochhammer[1/8, n] * Pochhammer[3/8, n] * Pochhammer[5/8, n] * Pochhammer[7/8, n] / Factorial[n]^5 * (15 + 304*n + 1920*n^2) / 7^(4*n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__92__1302.0548__transart2013-02-19.tex__671.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 93 *)
s[j_] := (-1/324)^j * (1/(3*(4*j + 1)) + 1/(9*(4*j + 2)) + 1/(54*(4*j + 3)));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__93__1304.0753__AGeneralizationOfTheShaferFinkInequality.tex__277.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 94 *)
s[j_] := (-1/829440000)^j * (1/(60*(4*j + 1)) + 1/(7200*(4*j + 2)) + 1/(1728000*(4*j + 3)));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__94__1304.0753__AGeneralizationOfTheShaferFinkInequality.tex__277.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 95 *)
s[k_] := 1/k^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__95__1310.5610__EE.tex__242.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 96 *)
s[k_] := 1/k^4;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__96__1310.5610__EE.tex__309.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 97 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__97__1310.5610__EE.tex__724.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 98 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__98__1310.5610__EE.tex__724.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 99 *)
s[m_] := 1/16^m * (4/(8*m + 1) - 2/(8*m + 4) - 1/(8*m + 5) - 1/(8*m + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__99__1410.5514__Multiple-correction_II_-2014-10-12.tex__58.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 100 *)
s[m_] := ((2 m)!)^3 / (m!)^6 * (42 m + 5) / 4096^m;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__100__1410.5514__Multiple-correction_II_-2014-10-12.tex__196.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 101 *)
s[m_] := 2/27 * 1/729^m * (243/(12*m + 1)^2 - 405/(12*m + 2)^2 - 81/(12*m + 4)^2 - 27/(12*m + 5)^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__101__1410.5514__Multiple-correction_II_-2014-10-12.tex__741.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 102 *)
s[n_] := (-1)^n / (2^(10 n) * (2 n + 1) * Binomial[2 n, n]^5);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__102__1504.01769__AMO-010.tex__501.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 103 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__103__1511.08568__ErrorAlternatingSeries.tex2.2.tex__141.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 104 *)
s[k_] := (4 k^2)/(4 k^2 - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__104__1511.09217__ChenParisWallis.tex__97.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 105 *)
s[j_] := 1 - 1/(4 j^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__105__1511.09217__ChenParisWallis.tex__171.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 106 *)
s[j_] := E^(1/j) * (1 - 1/(2*j))^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__106__1511.09217__ChenParisWallis.tex__190.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 107 *)
s[n_] := Binomial[2 n, n]^3 * (n + 1/6) / 256^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__107__1512.04608__HolonomicAlchemy-2016-08-17a.tex__504.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 108 *)
s[n_] := Binomial[2 n, n]^3 * (n + 5/42) / 4096^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__108__1512.04608__HolonomicAlchemy-2016-08-17a.tex__510.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 109 *)
s[k_] := Binomial[3 k, k] * Binomial[2 k, k]^2 * (k + 2/15) / (2^k * 3^(6 k));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__109__1512.04608__HolonomicAlchemy-2016-08-17a.tex__608.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 110 *)
s[k_] := (-1)^(k + 1) / (k * (k - 1) * (2*k - 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__110__1601.03180__ChenParisSeries-v14.tex__363.json",
	2,
	200,
	"series"
];

ClearAll[n];

(* 111 *)
s[n_] := (-1)^n / (2 n + 1)^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__111__1603.06709__2015multiple_angle_ver5.tex__993.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 112 *)
s[k_] := Binomial[2 k, k]^3 * (1/4 + k) * (-1/64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__112__1604.01106__MFE2016-04-05arXiv.tex__695.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 113 *)
s[k_] := Binomial[2 k, k]^3 * (1/6 + k) * (1/256)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__113__1604.01106__MFE2016-04-05arXiv.tex__712.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 114 *)
s[k_] := Binomial[2 k, k]^3 * (5/42 + k) * (1/4096)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__114__1604.01106__MFE2016-04-05arXiv.tex__720.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 115 *)
s[n_] := Pochhammer[1/2, n]^3 / (Factorial[n]^3) * (n + 5/42) * (1/2)^(6*n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__115__1609.07276__HyperModEqs_2016-09-23.tex__66.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 116 *)
s[k_] := Binomial[2 k, k]^3 * (k + 1/4) * (-1/64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__116__1609.07276__HyperModEqs_2016-09-23.tex__1361.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 117 *)
s[n_] := 27 * 16^n / ((2*n + 3)^3 * (2*n + 1)^2 * Binomial[2*n, n]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__117__1708.04269__Thai.tex__157.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 118 *)
s[n_] := 16^n / ((2 n + 1)^2 (2 n + 3)^2 Binomial[2 n, n]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__118__1708.04269__Thai.tex__162.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 119 *)
s[n_] := 16^n / (n^2 * (2*n + 1)^2 * Binomial[2*n, n]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__119__1708.04269__Thai.tex__162.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 120 *)
s[n_] := (-1/64)^n * (4*n + 1) * Binomial[2*n, n]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__120__1710.03221__CampbellDAurizioSondow4p7.tex__411.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 121 *)
s[k_] := Binomial[4 k, 2 k] * Binomial[2 k, k] / (k * 64^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__121__1710.03221__CampbellDAurizioSondow4p7.tex__1192.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 122 *)
s[k_] := (-1)^k * (4*k + 1) * (1/2)^(k^3) / Factorial[k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__122__1802.04616__q1overpi03g.tex__87.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 123 *)
s[k_] := ((1/2)^k)^2 / (Factorial[k] * Factorial[k + 1]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__123__1804.08210__Two_q-summation_formulas_and_q-analogues_of_series_expansions_for_certain_constants.tex__313.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 124 *)
s[n_] := Pochhammer[1/2, n]^2 / (Factorial[n] * Factorial[n + 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__124__1804.08210__Two_q-summation_formulas_and_q-analogues_of_series_expansions_for_certain_constants.tex__331.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 125 *)
s[n_] := (Pochhammer[1/2, n]^2) / (Factorial[n + 1]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__125__1804.08210__Two_q-summation_formulas_and_q-analogues_of_series_expansions_for_certain_constants.tex__353.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 126 *)
s[n_] := (Pochhammer[1/2, n]^2) / (Factorial[n + 1] * Factorial[n + 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__126__1804.08210__Two_q-summation_formulas_and_q-analogues_of_series_expansions_for_certain_constants.tex__365.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 127 *)
s[m_] := (-1)^(m + 1) * 1 / Factorial[2*m - 1] * Integrate[Exp[t]*t^(2*m - 1)/(Exp[2*t] - 1), {t, 0, Infinity}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__127__1806.07762__Dirichlet-lambda-function8.tex__483.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 128 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__128__1809.00998__Dalzell_Leibniz.tex__48.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 129 *)
s[m_] := m^(-2/(4 m^2 - 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__129__1810.10461__CosetStabilityRing.tex__215.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 130 *)
s[k_] := (4 k + 1) * (1/2)^k^3 / Factorial[k]^3 * (-1)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__130__1812.11322__q-clausen01q.tex__51.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 131 *)
s[k_] := (1/2)^k^3 / Factorial[k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__131__1812.11322__q-clausen01q.tex__94.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 132 *)
s[k_] := Pochhammer[1/2, k]^3 / Factorial[k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__132__1812.11322__q-clausen01q.tex__105.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 133 *)
s[k_] := (1 - 1/(4 k^2))^(-1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__133__1903.07407__2017applications_revised_arxiv.tex__226.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 134 *)
s[n_] := Pochhammer[1/2, n] * Pochhammer[1/4, n] * Pochhammer[3/4, n] / (Factorial[n]^3) * (40 n + 3) / (7^(4 n));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__134__1906.07384__hgm-asai-021920.tex__1145.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 135 *)
s[n_] := (1/2)^n^7 / Factorial[n]^7 * (168 n^3 + 76 n^2 + 14 n + 1) / 2^(6 n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__135__1906.07384__hgm-asai-021920.tex__1160.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 136 *)
s[n_] := (Pochhammer[1/2, n]^7 * Pochhammer[1/4, n] * Pochhammer[3/4, n] / Factorial[n]^9) * (43680*n^4 + 20632*n^3 + 4340*n^2 + 466*n + 21) / 2^(12*n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__136__1906.07384__hgm-asai-021920.tex__1170.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 137 *)
s[n_] := (Pochhammer[1/2, n]^5 * Pochhammer[1/3, n] * Pochhammer[2/3, n] * Pochhammer[1/4, n] * Pochhammer[3/4, n] / Factorial[n]^9) * (4528 n^4 + 3180 n^3 + 972 n^2 + 147 n + 9) * (-27/256)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__137__1906.07384__hgm-asai-021920.tex__1170.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 138 *)
s[k_] := ((2 k + 2)^2)/((2 k + 1) (2 k + 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__138__1909.00058__qUmbraPaper.tex__309.json",
	0,
	200,
	"product"
];

ClearAll[n];

(* 139 *)
s[m_] := 1/16^m * (4/(8*m + 1) - 2/(8*m + 4) - 1/(8*m + 5) - 1/(8*m + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__139__1910.04328__The_MC_Algorithm_and_its_applications-2019-10-10.tex__92.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 140 *)
s[k_] := 4 k/(16^k (k + 1)^2) * Binomial[2 k, k]^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__140__2005.04672__subm2020_arxiv.tex__386.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 141 *)
s[n_] := HarmonicNumber[n - 1] / n^3 * 4^(-n) * Binomial[2 n, n];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__141__2007.03957__one-dim_polylog_int.tex__406.json",
	2,
	200,
	"series"
];

ClearAll[n];

(* 142 *)
s[n_] := 1/(n^4 * (4^(-n) * Binomial[2*n, n])^(-2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__142__2007.03957__one-dim_polylog_int.tex__516.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 143 *)
s[k_] := (-1)^k / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__143__2007.10161__AKR-RBP1-V6.tex__74.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 144 *)
s[k_] := (-1)^k / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__144__2007.10161__AKR-RBP1-V6.tex__193.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 145 *)
s[k_] := k^2 * E^(-Pi * k^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__145__2009.00446__EiSum2.tex__1631.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 146 *)
s[k_] := (k/(k + 1))^((-1)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__146__2109.01477__Mizuno-type_formula7.tex__377.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 147 *)
s[n_] := (-1)^n * Factorial[6*n] * (13591409 + 545140134*n) / (Factorial[3*n] * Factorial[n]^3 * 640320^(3*n + 3/2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__147__2109.08392__gamma.tex__2889.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 148 *)
s[k_] := (2 k)/(2 k - 1) * (2 k)/(2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__148__2109.08686__Paper_arXiv.tex__337.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 149 *)
s[k_] := (1/2)^k * 1^k * 1^k / ((3/2)^k * (3/2)^k) * 1/Factorial[k] * (-1/4)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__149__2204.05647__Combinatorial_summation.tex__736.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 150 *)
s[r_] := Binomial[r - 1/2, r] * Pochhammer[1/2, r] / Pochhammer[3/2, r];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__150__2207.05551__UMGaussian_arxiv.tex__554.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 151 *)
s[k_] := k / (E^(2 k Pi) + 1) - 1/2 * k / (E^(k Pi) - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__151__2209.12658__DK03.tex__194.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 152 *)
s[n_] := -2 * (2^(-4))^n * Binomial[2*n, n] * (6*n + 5) / ((2*n + 3) * (2*n + 1) * (2*n - 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__152__2212.09965__AccelerationV30.tex__337.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 153 *)
s[n_] := (2^(-8))^n * Binomial[2*n, n]^3 * n^2 / ((2*n - 1)*(2*n - 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__153__2212.09965__AccelerationV30.tex__337.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 154 *)
s[k_] := (14 k + 11) (2 k + 1) (3 k + 1) Binomial[2 k, k] / ((4 k + 3) (4 k + 1)^2 (2 k - 1) Binomial[4 k, 2 k]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__154__2212.09965__AccelerationV30.tex__349.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 155 *)
s[n_] := (2^(-12))^n * Binomial[2*n, n]^3 * (6*n + 1) * (14*n - 3) * (2*n + 1) / (2*n - 1)^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__155__2212.09965__AccelerationV30.tex__349.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 156 *)
s[k_] := 2^(4 k) * (14 k^2 + 11 k + 1) * (k + 1) / (k * (4 k + 3) * (4 k + 1)^2 * (2 k - 1) * Binomial[2 k, k] * Binomial[4 k, 2 k]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__156__2212.09965__AccelerationV30.tex__349.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 157 *)
s[j_] := (-2^4)^j * (40*j^2 - 12*j - 1) * Binomial[2*j, j] / (j * (2*j - 1)^2 * (4*j + 1) * Binomial[4*j, 2*j]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__157__2212.09965__AccelerationV30.tex__426.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 158 *)
s[k_] := ((1/2)^k)^5 * ((1/3)^k) * ((2/3)^k) * ((1/4)^k) * ((3/4)^k) / (1^k)^9 * (4528 k^4 + 3180 k^3 + 972 k^2 + 147 k + 9) * (-27/256)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__158__2212.09965__AccelerationV30.tex__674.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 159 *)
s[n_] := (-1/64)^n * Binomial[2*n, n]^3 * (4*n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__159__2212.13305__ComplexV8.tex__69.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 160 *)
s[n_] := (1/2) * (1/4)^n * Binomial[2*n, n] / (4*n + 1)^2 + (9/8) * (1/4)^n * Binomial[2*n, n] / (4*n - 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__160__2304.00360__HalfV26.tex__669.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 161 *)
s[n_] := (9/8) * (1/4)^n * Binomial[2*n, n] / (4*n - 3) - (3/4) * (1/4)^n * Binomial[2*n, n] / (4*n - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__161__2304.00360__HalfV26.tex__688.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 162 *)
s[n_] := (1/4)^n * Binomial[2*n, n] * 1/(4*n - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__162__2304.00360__HalfV26.tex__704.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 163 *)
s[n_] := (1/2) * (1/4)^n * Binomial[2*n, n] / (4*n + 1)^2 + (9/8) * (1/4)^n * Binomial[2*n, n] / (4*n - 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__163__2304.00360__HalfV26.tex__704.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 164 *)
s[n_] := (1/4)^n * Binomial[2*n, n] * (9/(8*(4*n - 3)) - 3/(4*(4*n - 1)));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__164__2304.00360__HalfV26.tex__722.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 165 *)
s[n_] := (1/4)^n * Binomial[2*n, n] * (9/(8*(4*n - 3)) - 3/(4*(4*n - 1)));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__165__2304.00360__HalfV26.tex__737.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 166 *)
s[n_] := (9/8) * (1/4)^n * Binomial[2*n, n] / (4*n - 3) - (3/4) * (1/4)^n * Binomial[2*n, n] / (4*n - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__166__2304.00360__HalfV26.tex__752.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 167 *)
s[n_] := (1/4)^n * Binomial[2 n, n] / (4 n + 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__167__2304.00360__HalfV26.tex__759.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 168 *)
s[n_] := (1/4)^n * Binomial[2*n, n] * (1/(n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__168__2304.00360__HalfV26.tex__759.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 169 *)
s[j_] := (4/27)^j * (1/2 * 3/4 * 3/4 * 5/4 * 5/4) / (1 * 4/3 * 5/3 * 2 * 2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__169__2305.00626__FreeV48.tex__173.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 170 *)
s[n_] := (1/4)^n * HypergeometricPFQ[{1/2, 1/2, 1/2}, {1, 1, 1}, 1];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__170__2305.00626__FreeV48.tex__262.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 171 *)
s[n_] := (-1)^(n - 1) / (2 n - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__171__2307.05607__chapter6.tex__1276.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 172 *)
s[n_] := (-1/8)^n * (Pochhammer[1, n])^3 / ((Pochhammer[1/2, n])^3 * n^3) * (3*n - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__172__2312.14051__article.tex__679.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 173 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__173__2312.17402__chapter7_2.tex__278.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 174 *)
s[k_] := (350 k - 17) * Binomial[2 k, k] * 8^k / (Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__174__2401.14197__SunZhou2.tex__424.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 175 *)
s[k_] := (50 k - 7) * Binomial[2 k, k] * 8^k / (k * Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__175__2401.14197__SunZhou2.tex__431.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 176 *)
s[k_] := 2*((350*k - 17)*Binomial[2*k, k]*8^k)/(Binomial[3*k, k]*Binomial[6*k, 3*k]) - 7*((100*k^2 - 112*k + 15)*Binomial[2*k, k]*8^k)/(k*Binomial[3*k, k]*Binomial[6*k, 3*k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__176__2401.14197__SunZhou2.tex__570.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 177 *)
s[k_] := (50 k - 7) * Binomial[2 k, k] * 8^k / (k * Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__177__2401.14197__SunZhou2.tex__570.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 178 *)
s[k_] := (50*k - 7)*Binomial[2*k, k]*8^k/(k*Binomial[3*k, k]*Binomial[6*k, 3*k]) - (100*k^2 - 104*k + 15)*Binomial[2*k, k]*8^k/(k*(2*k - 1)*Binomial[3*k, k]*Binomial[6*k, 3*k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__178__2401.14197__SunZhou2.tex__584.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 179 *)
s[k_] := (5 k - 1) Binomial[2 k, k] 8^k / (k (2 k - 1) Binomial[3 k, k] Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__179__2401.14197__SunZhou2.tex__584.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 180 *)
s[k_] := Binomial[2 k, k] * 2^(3 k) / ((2 k - 1) * Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__180__2401.14197__SunZhou2.tex__651.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 181 *)
s[n_] := (2/3)^n * (2/3)^n * (3 n + 2) / ((-8)^n * (7/6)^n * (5/3)^n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__181__2402.08693__2024_01_04_2261101fad65ac5d3891g.tex__415.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 182 *)
s[i_] := 1/((2 i - 1) (i + 1)) * ((2 i - 1)!!/(2 i)!!) ^ 2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__182__2403.04944__PrePrint_arXiv-The_area_of_Hugelschaffer_curves_via_Taylor_series.TeX__1142.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 183 *)
s[n_] := Pochhammer[1/2, n]^2 / Pochhammer[1/2, n + 1]^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__183__2403.09729__sn-article_for_arXiv.tex__705.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 184 *)
s[k_] := (Factorial[k])^2 * 2^k / Factorial[2*k] * (-1/2 * 1/(k + 1) + 1/3 * 1/(k + 2) - 1/10 * 1/(k + 3) + 8/15 * 1/(2*k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__184__2403.09729__sn-article_for_arXiv.tex__952.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 185 *)
s[k_] := (Factorial[k])^2 / (Factorial[2 k] * (k + 1) * (k + 2) * (k + 3) * (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__185__2403.09729__sn-article_for_arXiv.tex__952.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 186 *)
s[k_] := (1/64)^k * (1/(5/4) + 1/(7/4));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__186__2405.02776__ShiftedV147.tex__290.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 187 *)
s[k_] := (-1)^k / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__187__2409.06658__partial-fractions-2.5.tex__135.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 188 *)
s[k_] := 1/(2 k + 1) * (1/(1 - 2 I))^(2 k + 1) - 1/(2 k + 1) * (1/(1 + 2 I))^(2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__188__2409.10097__2024-09-17_BBPbase5.tex__76.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 189 *)
s[k_] := 1 / (16 k^2 - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__189__2411.00280__main.tex__98.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 190 *)
s[n_] := (-1/27)^n * (9/(6*n + 1)^4 - 15/(6*n + 2)^4 - 18/(6*n + 3)^4 - 5/(6*n + 4)^4 + 1/(6*n + 5)^4);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__190__hep-th_slash_9803091__d3.tex__2395.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 191 *)
s[n_] := (-1/27)^n * (9/(6*n + 1)^2 - 15/(6*n + 2)^2 - 18/(6*n + 3)^2 - 5/(6*n + 4)^2 + 1/(6*n + 5)^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__191__hep-th_slash_9803091__d3.tex__2413.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 192 *)
s[k_] := -72/(12 k + 6)^2 - 9/(12 k + 7)^2 - 9/(12 k + 8)^2 - 5/(12 k + 10)^2 + 1/(12 k + 11)^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__192__hep-th_slash_9803091__d3.tex__2552.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 193 *)
s[n_] := (1/729)^n * (243/(12*n + 1)^4 - 405/(12*n + 2)^4 - 81/(12*n + 4)^4 - 27/(12*n + 5)^4);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__193__hep-th_slash_9803091__d3.tex__2578.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 194 *)
s[k_] := -72/(12 k + 6)^4 - 9/(12 k + 7)^4 - 9/(12 k + 8)^4 - 5/(12 k + 10)^4 + 1/(12 k + 11)^4;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__194__hep-th_slash_9803091__d3.tex__2578.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 195 *)
s[k_] := (1 + 2/k)^(-k*(-1)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__195__math_slash_0308074__rama.tex__1046.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 196 *)
s[k_] := (50 k - 6) / (Binomial[3 k, k] * 2^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__196__math_slash_0503507__detcomp.tex__2024.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 197 *)
s[n_] := (-1)^n / ((4*n + 1) * 4^n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__197__math_slash_0508170__e706.tex__120.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 198 *)
s[n_] := (-1)^n / ((4*n + 1) * 64^n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__198__math_slash_0508170__e706.tex__216.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 199 *)
s[k_] := (1/2)^5 * (20 k^2 + 8 k + 1) * (-1/4)^k / Factorial[k]^5;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__199__math_slash_0509465__quadr02a.tex__48.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 200 *)
s[k_] := (4 k^2)/(4 k^2 - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__200__math_slash_0610499__euler_alt_newestt11.tex__846.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 201 *)
s[k_] := (4 k^2 - 1)/(4 k^2)^((-1)^(k - 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_math.CA_0-22736/recurrence__201__math_slash_0610499__euler_alt_newestt11.tex__853.json",
	1,
	200,
	"product"
];

ClearAll[n];
*)



(* ::Text:: *)
(*421641-435736*)


(*
(* 0 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__0__math_slash_0006141__repr.tex__904.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 1 *)
s[n_] := 1 / ((n + 1) * (2 * n + 1) * (4 * n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__1__math_slash_0312440__odp.tex__1750.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 2 *)
s[n_] := (-1)^(n - 1) / (2 n - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__2__math_slash_0402462__polycf5jan2004df.tex__652.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 3 *)
s[n_] := 1 / ((n + 1) * (2 * n + 1) * (4 * n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__3__math_slash_0502582__MahdiaPeriodesNT0502582.tex__737.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 4 *)
s[k_] := Binomial[2 k, k]^3 / 2^(12 k) * (42 k + 5);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__4__math_slash_0503345__wz-bs.tex__93.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 5 *)
s[n_] := (-1)^n * Binomial[4*n, 2*n] * Binomial[2*n, n]^2 / 2^(10*n) * (20*n + 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__5__math_slash_0503345__wz-bs.tex__93.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 6 *)
s[n_] := (-1)^n * (1/2)^3 * (1/2)^3 / (Factorial[n])^3 * (1/4)^2 * (1/4)^2 * 2^(-12*n) * (26240*n^4 + 41184*n^3 + 21448*n^2 + 4170*n + 279) / ((8*n + 1)^2 * (8*n + 5)^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__6__math_slash_0503345__wz-bs.tex__179.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 7 *)
s[n_] := (1/8) * ((1/2)^n)^3 * ((1/4)^(2*n)) / (Factorial[n]^3 * ((1/4)^n)^2 * 2^(6*n)) * (240*n^2 + 110*n + 11) / (4*n + 1)^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__7__math_slash_0503345__wz-bs.tex__179.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 8 *)
s[k_] := (50 k - 6) / (Binomial[3 k, k] * 2^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__8__math_slash_0503507__detcomp.tex__2024.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 9 *)
s[n_] := (-1)^n / (4^n * (4 n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__9__math_slash_0508170__e706.tex__120.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 10 *)
s[n_] := (-1)^n / ((4*n + 1) * 64^n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__10__math_slash_0508170__e706.tex__216.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 11 *)
s[k_] := (1/2)^5 * (20 k^2 + 8 k + 1) * (-1/4)^k / Factorial[k]^5;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__11__math_slash_0509465__quadr02a.tex__48.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 12 *)
s[k_] := (4 k^2)/(4 k^2 - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__12__math_slash_0610499__euler_alt_newestt11.tex__846.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 13 *)
s[k_] := (4 k^2 - 1)/(4 k^2)^((-1)^(k - 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_421641-435736/recurrence__13__math_slash_0610499__euler_alt_newestt11.tex__853.json",
	1,
	200,
	"product"
];

ClearAll[n];

*)


(* ::Text:: *)
(*0-154047*)


(*
(* 0 *)
s[n_] := (-1)^n * (3*n + 1) / 32^n * Sum[Binomial[2*n - 2*k, n - k] * Binomial[2*k, k] * Binomial[n, k]^2, {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__0__0704.2438__threevariablemahlermeasures.tex__203.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 1 *)
s[n_] := (-1)^n * (3*n + 1) / 32^n * Sum[Binomial[2*n - 2*k, n - k] * Binomial[2*k, k] * Binomial[n, k]^2, {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__1__0704.2438__threevariablemahlermeasures.tex__757.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 2 *)
s[n_] := (-1)^n * Factorial[6*n] * (13591409 + 54513013*n) / (Factorial[n]^3 * Factorial[3*n] * (640320^3)^(n + 1/2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__2__0704.2438__threevariablemahlermeasures.tex__783.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 3 *)
s[k_] := (20 k + 3) * Pochhammer[1/4, k] * Pochhammer[1/2, k] * Pochhammer[3/4, k] / (Factorial[k]^3) * ((-1/4)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__3__0704.2438__threevariablemahlermeasures.tex__931.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 4 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__4__0708.2564__0708.2564.tex__99.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 5 *)
s[k_] := (-1)^k * (6*k + 1) / 4^k * Binomial[-1/2, k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__5__0708.3307__p-adicAnalogue.tex__112.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 6 *)
s[n_] := ((1/2)^n)^3 / (Factorial[n]^3) * (4*n + 1) * (-1)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__6__0712.1332__rampery2e-xxx.tex__131.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 7 *)
s[n_] := Pochhammer[1/2, n] * Pochhammer[1/4, n] * Pochhammer[3/4, n] / (Factorial[n]^3) * (20 n + 3) * (-1)^n / 2^(2 n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__7__0805.2788__exp01n.tex__149.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 8 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1) * 16^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__8__0807.0872__histoPi-fin-1.tex__85.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 9 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__9__0807.0872__histoPi-fin-1.tex__112.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 10 *)
s[k_] := Factorial[2 k]^3 / Factorial[k]^6 * 1/2^(12 k) * (42 k + 5);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__10__0807.0872__histoPi-fin-1.tex__267.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 11 *)
s[k_] := Factorial[2 k]^3 / Factorial[k]^6 * 1/2^(8 k) * (6 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__11__0807.0872__histoPi-fin-1.tex__267.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 12 *)
s[n_] := Factorial[2 n] * Factorial[3 n] / (Factorial[n]^5 * 1458^n) * (15 n + 2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__12__0807.0872__histoPi-fin-1.tex__280.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 13 *)
s[n_] := 1/16^n * (4/(8*n + 1) - 2/(8*n + 4) - 1/(8*n + 5) - 1/(8*n + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__13__0807.0872__histoPi-fin-1.tex__350.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 14 *)
s[n_] := (-1)^n / 4^n * (2/(4 n + 1) + 2/(4 n + 2) + 1/(4 n + 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__14__0807.0872__histoPi-fin-1.tex__368.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 15 *)
s[n_] := (-1)^n / (4^n (2 n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__15__0807.0872__histoPi-fin-1.tex__380.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 16 *)
s[n_] := (1^((-1)^1 * Binomial[n, 0]) * 2^((-1)^2 * Binomial[n, 1]) * (n + 1)^((-1)^(n + 1) * Binomial[n, n]))^(1/2^n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__16__0807.0872__histoPi-fin-1.tex__439.json",
	0,
	200,
	"product"
];

ClearAll[n];

(* 17 *)
s[k_] := Factorial[2 k]^3 / Factorial[k]^6 * 1/2^(8 k) * (6 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__17__0807.0872__histoPi-fin-1.tex__507.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 18 *)
s[k_] := (-1)^k * (4*k + 1) * (1/2)^(k^3) / Factorial[k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__18__0903.0400__Ramanujan32DZ.tex__52.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 19 *)
s[k_] := Binomial[2 k, k]^3 * (6 k + 1) / 2^(8 k + 4);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__19__0906.5560__soda4.tex__1396.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 20 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__20__0906.5560__soda4.tex__1676.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 21 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__21__0906.5560__soda4.tex__1685.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 22 *)
s[k_] := (4/(8 k + 1) - 2/(8 k + 4) - 1/(8 k + 5) - 1/(8 k + 6))*(1/16)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__22__0906.5560__soda4.tex__1867.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 23 *)
s[n_] := 1 / ((n + 1) * (2 * n + 1) * (4 * n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__23__0909.2387__yuanli3.tex__145.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 24 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1) * 4^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__24__0911.2415__135b.tex__90.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 25 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1) * 4^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__25__0911.2415__135b.tex__112.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 26 *)
s[k_] := Binomial[2 k, k] / ((2 k + 1) * 16^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__26__0911.2415__135b.tex__553.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 27 *)
s[k_] := (20 k + 3) / ((-2^10)^k * Binomial[4 k, k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__27__0911.5665__SunConj.tex__516.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 28 *)
s[k_] := (260 k + 23) * Pochhammer[1/2, k] * Pochhammer[1/4, k] * Pochhammer[3/4, k] / (Factorial[k]^3 * 18^(2 k));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__28__0911.5665__SunConj.tex__558.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 29 *)
s[k_] := (21460 k + 1123) / ((-2^10 * 21^4)^k * Binomial[4 k, k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__29__0911.5665__SunConj.tex__588.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 30 *)
s[k_] := (4 k + 1) / ((-64)^k * Binomial[2 k, k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__30__0911.5665__SunConj.tex__786.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 31 *)
s[k_] := (7 k + 1)/(648^k) * Binomial[4 k, k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__31__0911.5665__SunConj.tex__919.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 32 *)
s[k_] := (357 k + 103)/2160^k * Binomial[2 k, k] * Sum[Binomial[k, j] * Binomial[k + 2 j, 2 j] * Binomial[2 j, j] * (-324)^(k - j), {j, 0, k}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__32__0911.5665__SunConj.tex__1196.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 33 *)
s[k_] := (25 k - 3) / (2^k Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__33__0911.5665__SunConj.tex__1349.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 34 *)
s[k_] := (4 k + 1) * (1/2^k / Factorial[k])^3 * (-1)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__34__0912.0197__Ramanujan-Type-Supper-10-15-10.tex__123.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 35 *)
s[k_] := Binomial[2 k, k] * 2^(-2 k) / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__35__1004.2453__ws.tex__232.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 36 *)
s[k_] := (4 k + 1) / ((-64)^k * Binomial[2 k, k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__36__1004.4623__143d.tex__178.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 37 *)
s[k_] := (20 k + 3) * Binomial[2 k, k]^2 * Binomial[4 k, 2 k] / (-2^10)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__37__1004.4623__143d.tex__180.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 38 *)
s[k_] := 1/2^(4 k) * (4/(8 k + 1) - 2/(8 k + 4) - 1/(8 k + 5) - 1/(8 k + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__38__1008.3171__2e15bit_of_pi.tex__131.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 39 *)
s[k_] := (-1)^k / 2^(10 k) * (2^2 / (10 k + 1) - 1 / (10 k + 3) - 2^(-4) / (10 k + 5) - 2^(-4) / (10 k + 7) + 2^(-6) / (10 k + 9) - 2^(-1) / (4 k + 1) - 2^(-6) / (4 k + 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__39__1008.3171__2e15bit_of_pi.tex__146.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 40 *)
s[k_] := (-1)^k / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__40__1010.4298__165s.tex__212.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 41 *)
s[k_] := (4 k + 1) Binomial[-1/2, k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__41__1011.1902__140m.tex__111.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 42 *)
s[k_] := (20 k + 3) / ((-2^10)^k * Binomial[4 k, k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__42__1011.1902__140m.tex__149.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 43 *)
s[k_] := (7 k + 1) / (648^k) * Binomial[4 k, k];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__43__1011.1902__140m.tex__163.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 44 *)
s[k_] := (4 k + 1) * Binomial[2 k, k]^3 / (-64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__44__1101.0600__151n.tex__200.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 45 *)
s[k_] := (25 k - 3) / (2^k Binomial[3 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__45__1101.0600__151n.tex__228.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 46 *)
s[k_] := (30 k + 7) / ((-256)^k * Binomial[2 k, k]^2 * T_k[1, 16]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__46__1101.0600__151n.tex__766.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 47 *)
s[n_] := (21 n + 1)/64^n * Sum[Binomial[n, k] * Binomial[2 k, n] * Binomial[2 k, k] * Binomial[2 n - 2 k, n - k] * 3^(2 k - n), {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__47__1102.5649__ConjSeries.tex__372.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 48 *)
s[n_] := (9 k + 1)/64^k * Sum[Binomial[-1/4, k]^2 * Binomial[-3/4, n - k]^2, {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__48__1102.5649__ConjSeries.tex__487.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 49 *)
s[k_] := (4 k + 1) / ((-64)^k * Binomial[2 k, k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__49__1103.4325__141c.tex__323.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 50 *)
s[k_] := (357 k + 103)/2160^k * Binomial[2 k, k] * Sum[Binomial[k, j] * Binomial[k + 2 j, 2 j] * Binomial[2 j, j] * (-324)^(k - j), {j, 0, k}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__50__1103.4325__141c.tex__413.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 51 *)
s[n_] := (21 n + 1)/64^n * Sum[Binomial[n, k] * Binomial[2 k, n] * Binomial[2 k, k] * Binomial[2 n - 2 k, n - k] * 3^(2 k - n), {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__51__1103.4325__141c.tex__1290.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 52 *)
s[n_] := (16 n + 5)/(324^n) * Binomial[2 n, n] * Sum[Binomial[n, k]^2 * Binomial[2 k, k] * (-20)^k, {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__52__1103.4325__141c.tex__1369.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 53 *)
s[n_] := Binomial[2 n, n]^3 * (42 n + 5) / 2^(12 n + 4);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__53__1103.6022__gvalues.tex__448.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 54 *)
s[n_] := (-1)^n * Binomial[2*n, n]^3 / 2^(6*n) * (4*n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__54__1104.0392__RJ-generators.tex__226.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 55 *)
s[k_] := Binomial[2 k, k]^3 / 2^(8 k) * (6 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__55__1104.0392__RJ-generators.tex__227.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 56 *)
s[k_] := Binomial[2 k, k]^3 / 2^(8 k) * (6 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__56__1104.0392__RJ-generators.tex__228.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 57 *)
s[n_] := (-1)^n * Binomial[4*n, 2*n] * Binomial[2*n, n]^2 / 2^(10*n) * (20*n + 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__57__1104.0392__RJ-generators.tex__229.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 58 *)
s[n_] := (-1)^n * Binomial[4*n, 2*n] * Binomial[2*n, n]^2 / 2^(10*n) * (20*n + 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__58__1104.0392__RJ-generators.tex__232.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 59 *)
s[k_] := Binomial[2 k, k]^3 / 2^(12 k) * (42 k + 5);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__59__1104.0392__RJ-generators.tex__233.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 60 *)
s[k_] := 1/(2^(6 k)) * (1/2)^3 * (42 k + 5);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__60__1104.1994__arx-morehypiden-f5.tex__54.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 61 *)
s[n_] := n/54^n * Sum[Binomial[2*k, k] * Binomial[3*k, k] * Binomial[2*(n - k), n - k] * Binomial[3*(n - k), n - k], {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__61__1104.3856__157b.tex__128.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 62 *)
s[n_] := (9 n + 1)/64^n * Sum[Binomial[-1/4, k]^2 * Binomial[-3/4, n - k]^2, {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__62__1104.3856__157b.tex__175.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 63 *)
s[k_] := (7 k + 1) * Binomial[4 k, 2 k] * Binomial[2 k, k]^2 / 648^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__63__1104.3856__157b.tex__320.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 64 *)
s[k_] := Binomial[2 k, k] / ((-16)^k * (2 k + 1)^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__64__1110.5308__jacobiaperyFinalR3.tex__102.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 65 *)
s[k_] := 1/(2^(6 k)) * (1/2)^3 * (42 k + 5);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__65__1203.1255__arx-kind-rama-proofs-06.tex__51.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 66 *)
s[k_] := (2 k)^2 / ((2 k - 1) (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__66__1206.1801__zeta.tex__185.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 67 *)
s[n_] := (-1)^n / 2^(6 n) * Binomial[2 n, n]^3 * (1/2 + 2 n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__67__1206.3981__rama-updown2.tex__95.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 68 *)
s[k_] := 1/16^k * (4/(8*k + 1) - 2/(8*k + 4) - 1/(8*k + 5) - 1/(8*k + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__68__1209.2348__SaganNumbers.tex__263.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 69 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__69__1209.3657__history_of_characters.tex__835.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 70 *)
s[k_] := 1 - 1/(4 k^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__70__1209.5739__summClaculus6.tex__1343.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 71 *)
s[k_] := 1/(4 k - 3) - 1/(4 k - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__71__1209.5739__summClaculus6.tex__3001.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 72 *)
s[n_] := (1054 n + 233)/(480^n) * Binomial[2 n, n] * Sum[Binomial[n, k]^2 * Binomial[2 k, n] * (-1)^k * 8^(2 k - n), {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__72__1210.2373__sun520a.tex__96.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 73 *)
s[n_] := Binomial[2 n, n]^3 * (27 - 30 2^(1/3) + 6 2^(2/3) + (66 - 84 2^(1/3) + 12 2^(2/3)) n) / (2 (1 + 2^(1/3) + 2^(2/3)))^(8 n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__73__1211.6563__polytope.tex__1171.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 74 *)
s[n_] := Binomial[2 n, n]^2 * Binomial[3 n, n] * (12 + (68 - 4 I) n) / (-146 + 322 I)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__74__1211.6563__polytope.tex__1288.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 75 *)
s[k_] := (762300 - 300288*2^(1/3) - 223080*2^(2/3) + (721776 - 329760*2^(1/3) - 38880*2^(2/3))*k) / (1170 + 928*2^(1/3) + 736*2^(2/3))^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__75__1211.6563__polytope.tex__4013.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 76 *)
s[n_] := n/864^n * Sum[Binomial[6*k, 3*k] * Binomial[3*k, k] * Binomial[6*(n - k), 3*(n - k)] * Binomial[3*(n - k), n - k], {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__76__1301.4877__fourbino.tex__68.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 77 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__77__1302.0471__test.tex__880.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 78 *)
s[n_] := (1/48)^n * (1/2)^n * (1/4)^n * (3/4)^n / Factorial[n]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__78__1302.0548__transart2013-02-19.tex__373.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 79 *)
s[n_] := Sum[Binomial[n, j]^4 * (1 + 3 n) * (-1/20)^n, {j, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__79__1302.0548__transart2013-02-19.tex__435.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 80 *)
s[k_] := (4/(8 k + 1) - 2/(8 k + 4) - 1/(8 k + 5) - 1/(8 k + 6))*(1/16)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__80__1302.2898__turing.tex__445.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 81 *)
s[n_] := (Pochhammer[1/4, n] * Pochhammer[1/2, n] * Pochhammer[3/4, n]) / (Factorial[n]^3) * (32/81)^n * (1 + 7*n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__81__1302.5984__newpi.tex__262.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 82 *)
s[n_] := (Pochhammer[1/2, n]^3) / (Factorial[n]^3) * (1/4)^n * (1 + 6*n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__82__1302.5984__newpi.tex__265.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 83 *)
s[n_] := Binomial[6 n, 4 n] * Binomial[6 n, 3 n] * Binomial[4 n, 2 n] * (25 - 108 n^2) / ((6 n - 5)^2 * 2^(8 n) * 3^(6 n));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__83__1302.5984__newpi.tex__368.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 84 *)
s[k_] := (-1)^k / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__84__1303.1856__euler-arxiv6.tex__1228.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 85 *)
s[k_] := (Pochhammer[1/2, k]/Factorial[k])^3 * (6*k + 1) / 4^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__85__1303.6228__ASD-9-25-14.tex__481.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 86 *)
s[k_] := (1 + 2/k)^(k*(-1)^(k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__86__1305.6247__note-kachi-tzermias.tex__104.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 87 *)
s[k_] := (k + 1/2) * (k + 3/2) / (k + 1)^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__87__1305.6247__note-kachi-tzermias.tex__276.json",
	0,
	200,
	"product"
];

ClearAll[n];

(* 88 *)
s[k_] := (4 k^2)/(4 k^2 - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__88__1307.7434__Logaritmische_Integrale-_revisited.tex__113.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 89 *)
s[k_] := (-1)^k * Factorial[6*k] * (15591409 + 545140134*k) / (Factorial[3*k] * Factorial[k]^3 * 640320^(3*k + 3/2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__89__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__44.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 90 *)
s[n_] := (1/2)^n * (1/2)^n * (1/2)^n / (1)^n^3 * (4 n + 1) * (-1)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__90__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__375.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 91 *)
s[n_] := Pochhammer[1/2, n]^3 / Pochhammer[1, n]^3 * (4 n + 1) * (-1)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__91__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__415.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 92 *)
s[k_] := (1/2)^3 / 1^3 * (6 k + 1) * (1/4)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__92__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__530.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 93 *)
s[n_] := Pochhammer[1/2, n] * Pochhammer[1/4, n] * Pochhammer[3/4, n] / (Pochhammer[1, n]^3) * (7*n + 1) * (32/81)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__93__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__548.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 94 *)
s[n_] := ((1/2)^n)^3 / (1^n)^3 * (4 n + 1) * (-1)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__94__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__586.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 95 *)
s[k_] := (1/2)^3 * (42 k + 5) * (1/64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__95__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__599.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 96 *)
s[k_] := (1/2)^3 * (42 k + 5) * (1/64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__96__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__605.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 97 *)
s[n_] := (1/2)^3 * Factorial[n]^3 / Factorial[n]^3 * (42 n + 5) * (1/64)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__97__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__622.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 98 *)
s[n_] := (1/2)^3 * Factorial[n]^3 / Factorial[n]^3 * (42 n + 5) / 64^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__98__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__640.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 99 *)
s[n_] := (1/2)^n / (Factorial[n]^3) * (6 n + 1) * (-8)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__99__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__716.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 100 *)
s[k_] := (1/2)^3 * (6 k + 1) * (-8)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__100__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__729.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 101 *)
s[n_] := ((1/2)^n)^3 / (1^n)^3 * (6 n + 1) * (1/4)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__101__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__746.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 102 *)
s[n_] := (Pochhammer[1/2, n]^3 * (3*n + 1) * 4^n) / (Pochhammer[1, n]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__102__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__754.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 103 *)
s[n_] := (1/2)^3 * Factorial[n]^3 / Factorial[n]^3 * (21 n + 8) * 64^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__103__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__798.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 104 *)
s[n_] := Pochhammer[1/2, n]^3 / Pochhammer[1, n]^3 * (3*n + 1) * 2^(2*n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__104__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__817.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 105 *)
s[n_] := (1/2)^n * (1/4)^n * (3/4)^n / (1^n)^3 * (30 n + 8) * (4/3)^(4 n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__105__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__833.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 106 *)
s[k_] := (1/2)^3 * (4 k + 1) * (-1)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__106__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__979.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 107 *)
s[k_] := (1/2)^3 * (3 k + 1) * (-8)^k / (1)^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__107__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__996.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 108 *)
s[n_] := (1/2)^n^3 / (1)^n^3 * (6 n + 1) * (1/4)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__108__1309.1140__On_proving_some_of_Ramanujan_s_formulas_with_an_elementary_method.tex__1265.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 109 *)
s[j_] := (-1)^(j - 1) / (2*j - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__109__1406.1168__SUM.tex__472.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 110 *)
s[k_] := (2 k) (2 k) / ((2 k - 1) (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__110__1406.7407__prod-pliage.tex__111.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 111 *)
s[k_] := ((7 k - 1) * (-4)^k * Binomial[2 k, k]) / ((2 k - 1) * k * Binomial[3 k, k] * Binomial[6 k, 3 k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__111__1407.8465__224h.tex__737.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 112 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__112__1501.05457__cyclotomicv2.tex__71.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 113 *)
s[k_] := 1/(4 k - 3) - 1/(4 k - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__113__1501.05457__cyclotomicv2.tex__137.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 114 *)
s[n_] := Pochhammer[1/3, n] * Pochhammer[2/3, n] * Pochhammer[1/6, n] * Pochhammer[5/6, n] / (Pochhammer[1/2, n] * Factorial[n]^3) * (3/5)^(6*n) * (133*n^2 + 79*n + 6) / (2*n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__114__1501.06413__fam-rama-orr-arxiv-3.tex__263.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 115 *)
s[n_] := (1/10)^n * (3/10)^n * (7/10)^n * (9/10)^n / ((1/2)^n * 1^n^3) * 1/(2^(6*n)) * (2100*n^2 + 1160*n + 63)/(2*n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__115__1501.06413__fam-rama-orr-arxiv-3.tex__275.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 116 *)
s[n_] := Pochhammer[1/3, n] * Pochhammer[2/3, n] * Pochhammer[1/6, n] * Pochhammer[5/6, n] / (Pochhammer[1/2, n] * Factorial[n]^3) * (3/5)^(6*n) * (133*n^2 + 79*n + 6) / (2*n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__116__1501.06413__fam-rama-orr-arxiv-3.tex__656.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 117 *)
s[n_] := (Pochhammer[1/10, n] * Pochhammer[3/10, n] * Pochhammer[7/10, n] * Pochhammer[9/10, n]) / (Pochhammer[1/2, n] * Pochhammer[1, n]^3) * 1/(2^(6*n)) * (2100*n^2 + 1160*n + 63)/(2*n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__117__1501.06413__fam-rama-orr-arxiv-3.tex__668.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 118 *)
s[k_] := (4 k + 1) * (-1)^k * (1/2)^k^3 / Factorial[k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__118__1504.01028__vH-4-2-15.tex__65.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 119 *)
s[k_] := (4 k + 1) * (-1)^k * (1/2)^3 / k^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__119__1504.01028__vH-4-2-15.tex__96.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 120 *)
s[k_] := (1/2)^3 k / Factorial[k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__120__1504.01028__vH-4-2-15.tex__109.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 121 *)
s[k_] := 1/(k + 1) * (1/2)^2 * Factorial[k] / Factorial[k]^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__121__1504.01028__vH-4-2-15.tex__111.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 122 *)
s[k_] := (6 k + 1)/(4^k) * (1/2)^3 / Factorial[k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__122__1504.01028__vH-4-2-15.tex__113.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 123 *)
s[k_] := (42 k + 5)/(64^k) * (1/2)^3 * Binomial[3 k, k]/Factorial[k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__123__1504.01028__vH-4-2-15.tex__115.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 124 *)
s[n_] := ((1/2)^n)^3 / (Factorial[n]^3) * (42*n + 5) * (1/64)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__124__1504.01976__k2oz_accepted.tex__46.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 125 *)
s[k_] := (6 k + 1) * (Pochhammer[1/2, k]/Factorial[k])^3 * (1/4)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__125__1510.02575__Ch7-ClausenRamanujan.tex__150.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 126 *)
s[k_] := Binomial[2 k, k]^3 * (k + 1/6) / 256^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__126__1512.04608__HolonomicAlchemy-2016-08-17a.tex__504.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 127 *)
s[n_] := Binomial[2 n, n]^3 * (n + 5/42) / 4096^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__127__1512.04608__HolonomicAlchemy-2016-08-17a.tex__510.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 128 *)
s[k_] := Binomial[3 k, k] * Binomial[2 k, k]^2 * (k + 2/15) / (2^k * 3^(6 k));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__128__1512.04608__HolonomicAlchemy-2016-08-17a.tex__608.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 129 *)
s[r_] := 1 + 1/(4 r (r - 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__129__1601.02243__Dill,_Effective_Approximation.tex__200.json",
	2,
	200,
	"product"
];

ClearAll[n];

(* 130 *)
s[n_] := (-1)^(n - 1) / 4^n * (2/(4*n - 3) + 1/(2*n - 1) + 1/(4*n - 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__130__1603.08540__arctan_derivatives.tex__190.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 131 *)
s[n_] := (-1)^n / 4^n * (2/(4*n + 1) + 2/(4*n + 2) + 1/(4*n + 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__131__1603.08540__arctan_derivatives.tex__194.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 132 *)
s[n_] := 1/(16^n) * (4/(8*n + 1) - 2/(8*n + 4) - 1/(8*n + 5) - 1/(8*n + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__132__1603.08540__arctan_derivatives.tex__200.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 133 *)
s[n_] := (-1)^n / 4^n * (2/(4*n + 1) + 2/(4*n + 2) + 1/(4*n + 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__133__1603.08540__arctan_derivatives.tex__258.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 134 *)
s[k_] := (1/2)^k^3 / (1)^k^3 * (5 + 42 k) / 64^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__134__1604.00193__proof-algos-pi-arx.tex__75.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 135 *)
s[k_] := (1/2)^k^2 / 1^k^2 * 1/2^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__135__1604.00193__proof-algos-pi-arx.tex__197.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 136 *)
s[k_] := Binomial[2 k, k]^3 * (1/4 + k) * (-1/64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__136__1604.01106__MFE2016-04-05arXiv.tex__695.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 137 *)
s[k_] := Binomial[2 k, k]^3 * (1/6 + k) * (1/256)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__137__1604.01106__MFE2016-04-05arXiv.tex__712.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 138 *)
s[k_] := Binomial[2 k, k]^3 * (5/42 + k) * (1/4096)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__138__1604.01106__MFE2016-04-05arXiv.tex__720.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 139 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__139__1606.03186__BMdistprojSPADec8.tex__504.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 140 *)
s[j_] := (2 j) (2 j) / ((2 j - 1) (2 j + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__140__1606.07460__Sanayei_MS_From_e_to_Pi.tex__124.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 141 *)
s[k_] := (-1)^k * (545140134*k + 13591409) / (640320^3)^(k + 1/2) * Factorial[6*k] / (Factorial[3*k] * Factorial[k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__141__1609.05778__chen_glebov_revised.tex__64.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 142 *)
s[n_] := ((1/2)^n)^3 / (Factorial[n]^3) * (n + 5/42) * (1/2)^(6*n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__142__1609.07276__HyperModEqs_2016-09-23.tex__66.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 143 *)
s[k_] := Binomial[2 k, k]^3 * (k + 1/4) * (-1/64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__143__1609.07276__HyperModEqs_2016-09-23.tex__1361.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 144 *)
s[n_] := (-1)^n * Pochhammer[1/2, n] * Pochhammer[1/3, n] * Pochhammer[2/3, n] * Pochhammer[1/6, n] * Pochhammer[5/6, n] / Pochhammer[1, n]^5 * (3/4)^(6*n) * (1930*n^2 + 549*n + 45);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__144__1610.04839__bilater-rama-arx.tex__162.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 145 *)
s[n_] := (1/2)^n^5 / (1)^n^3 * (1/6)^n * (5/6)^n * (28 k^2 + 10 k + 1) / (6 k + 1) * (-1/27)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__145__1610.04839__bilater-rama-arx.tex__234.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 146 *)
s[n_] := (-1)^n * Pochhammer[1/2, n] * Pochhammer[1/4, n] * Pochhammer[3/4, n] / Pochhammer[1, n]^3 * (21460*n + 1123) / 882^(2*n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__146__1610.04839__bilater-rama-arx.tex__315.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 147 *)
s[k_] := ((1/2)^k)^3 / (Factorial[k]^3) * (3/2*k + 1/4) * 1/4^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__147__1611.02217__wronskians-pi.tex__986.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 148 *)
s[k_] := ((1/2)^k)^3 / (Factorial[k]^3) * (21/8 k + 5/16) * (1/64)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__148__1611.02217__wronskians-pi.tex__1056.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 149 *)
s[k_] := (-1)^k * Pochhammer[1/2, k] * Pochhammer[1/4, k] * Pochhammer[3/4, k] / Pochhammer[1, k]^3 * (1123 + 21460*k) * (1/882)^(2*k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__149__1611.02217__wronskians-pi.tex__2308.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 150 *)
s[k_] := 1 - 1/(4 k^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__150__1611.09877__6v-Free-energy-and-Correlation-Length-Edit3.tex__1555.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 151 *)
s[k_] := Binomial[2 k, k]^3 / 64^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__151__1701.00729__superhyp2arxivv3.tex__61.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 152 *)
s[k_] := (4 k + 1) * Binomial[2 k, k]^3 / 64^k * (-1)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__152__1701.00729__superhyp2arxivv3.tex__670.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 153 *)
s[k_] := (-1)^k / (2*k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__153__1704.02498__right_main_term_irreducible_v7.tex__158.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 154 *)
s[n_] := 16^n / ((2 n + 1)^2 (2 n + 3)^2 Binomial[2 n, n]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__154__1708.04269__Thai.tex__162.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 155 *)
s[n_] := 16^n / (n^2 * (2*n + 1)^2 * Binomial[2*n, n]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__155__1708.04269__Thai.tex__162.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 156 *)
s[n_] := (-1/64)^n * (4*n + 1) * Binomial[2*n, n]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__156__1710.03221__CampbellDAurizioSondow4p7.tex__411.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 157 *)
s[k_] := (6 k + 1) * Pochhammer[1/2, k] / (4^(k + 1) * Factorial[k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__157__1711.00456__Level_20_Update.tex__1105.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 158 *)
s[n_] := n * E^(3 * n * Pi / 2) / (E^(2 * n * Pi) - 1) + 2 * n * (-1)^n / (E^(4 * n * Pi) - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__158__1801.09181__dgkm_hz1_11.tex__512.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 159 *)
s[n_] := n E^(3 n \[Pi]/2)/(E^(2 n \[Pi]) - 1) + 2 n (-1)^n/(E^(4 n \[Pi]) - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__159__1801.09181__dgkm_hz1_11.tex__2089.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 160 *)
s[n_] := (-1)^(n - 1) / (2 n - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__160__1801.09181__dgkm_hz1_11.tex__2177.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 161 *)
s[k_] := (((1/2)^k)^3)/((1^k)^3) * (3*k + 1) * 2^(2*k) * (-2*I/Pi);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__161__1802.01260__qZudilin2.tex__79.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 162 *)
s[k_] := (Pochhammer[1/2, k]^3 / Pochhammer[1, k]^3) * (3*k + 1) * (-1)^k * 2^(3*k) / Pi;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__162__1802.01260__qZudilin2.tex__79.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 163 *)
s[k_] := (4 k^2)/(4 k^2 - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__163__1802.01473__188q.tex__140.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 164 *)
s[k_] := (-1)^k / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__164__1802.01473__188q.tex__152.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 165 *)
s[k_] := (-1)^k / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__165__1802.01506__189p.tex__149.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 166 *)
s[k_] := (-1)^k / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__166__1802.01506__189p.tex__192.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 167 *)
s[k_] := (6 k + 1) * Pochhammer[1/2, k]^3 / (Factorial[k]^3 * 4^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__167__1802.01506__189p.tex__208.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 168 *)
s[k_] := (-1)^k * (4*k + 1) * (1/2)^(k^3) / (Factorial[k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__168__1802.04616__q1overpi03g.tex__87.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 169 *)
s[n_] := Pochhammer[1/4, n] * Pochhammer[1/2, n] * Pochhammer[3/4, n] / Factorial[n]^3 * (1103 + 26390*n) / 99^(4*n + 2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__169__1802.07558__rpb269v3.tex__1323.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 170 *)
s[n_] := (-1)^n * Factorial[6 n] * (13591409 + 545140134 n) / (Factorial[3 n] * Factorial[n]^3 * 640320^(3 n + 3/2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__170__1802.07558__rpb269v3.tex__1333.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 171 *)
s[k_] := (4 k + 1) / ((-64)^k * Binomial[2 k, k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__171__1802.09798__Chen-RationalWZ-final.tex__198.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 172 *)
s[q_] := 3 / ((2 q + 1) * 2^(4 q)) * Binomial[2 q, q];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__172__1804.00394__final_arxiv.tex__2307.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 173 *)
s[k_] := 1 - 1/(4 k^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__173__1804.01447__CSP-Matrix.tex__511.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 174 *)
s[n_] := (1/2)^n^3 / (1)^n^3 * (1/64)^n * (42 n + 5);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__174__1804.02695__rama-termina-arx-01.tex__111.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 175 *)
s[n_] := Pochhammer[1/2, n] * Pochhammer[1/4, n] * Pochhammer[3/4, n] / Pochhammer[1, n]^3 * (32/81)^n * (7 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__175__1804.02695__rama-termina-arx-01.tex__151.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 176 *)
s[n_] := Pochhammer[1/2, n]^2 / (Factorial[n] * Factorial[n + 1]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__176__1804.08210__Two_q-summation_formulas_and_q-analogues_of_series_expansions_for_certain_constants.tex__313.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 177 *)
s[n_] := Pochhammer[1/2, n]^2 / (Factorial[n] * Factorial[n + 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__177__1804.08210__Two_q-summation_formulas_and_q-analogues_of_series_expansions_for_certain_constants.tex__331.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 178 *)
s[n_] := (Pochhammer[1/2, n]^2) / ((Factorial[n + 1])^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__178__1804.08210__Two_q-summation_formulas_and_q-analogues_of_series_expansions_for_certain_constants.tex__353.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 179 *)
s[n_] := (Pochhammer[1/2, n]^2) / (Factorial[n + 1] * Factorial[n + 2]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__179__1804.08210__Two_q-summation_formulas_and_q-analogues_of_series_expansions_for_certain_constants.tex__365.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 180 *)
s[k_] := ((1/2)^k)^2 / ((k + 1) * Factorial[k]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__180__1805.06568__GaussPifinalversion2018.tex__226.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 181 *)
s[n_] := Pochhammer[1/2, n]^2 / ((n + 1) (n + 2) Factorial[n]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__181__1805.06568__GaussPifinalversion2018.tex__231.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 182 *)
s[k_] := (1/2)^k^2 / ((k + 2) * Factorial[k + 1]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__182__1805.06568__GaussPifinalversion2018.tex__268.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 183 *)
s[k_] := (1/2)^k^2 / Factorial[n + 2]^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__183__1805.06568__GaussPifinalversion2018.tex__304.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 184 *)
s[n_] := (1/6)^n * (5/6)^n / Factorial[n + 1]^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__184__1805.06568__GaussPifinalversion2018.tex__390.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 185 *)
s[k_] := (2 k + 1)^2 / (2 k (2 k + 2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__185__1806.03346__Cfraction.tex__59.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 186 *)
s[n_] := (-1)^(n - 1) / (2 n - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__186__1806.03346__Cfraction.tex__93.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 187 *)
s[n_] := (-1)^(n - 1) / ((2*n - 1)*(2*n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__187__1806.03346__Cfraction.tex__106.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 188 *)
s[k_] := (2 k)/(2 k - 1) * (2 k)/(2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__188__1806.03346__Cfraction.tex__135.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 189 *)
s[n_] := Factorial[n] / Product[2*i + 1, {i, 1, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__189__1806.03346__Cfraction.tex__161.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 190 *)
s[n_] := (-1)^(n - 1) / ((2*n - 1)*(2*n + 1)*(2*n + 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__190__1806.03346__Cfraction.tex__194.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 191 *)
s[n_] := (-1)^(n - 1) / ((2*n - 1)*(2*n + 1)*(2*n + 3)*(2*n + 5));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__191__1806.03346__Cfraction.tex__198.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 192 *)
s[n_] := (-1)^(n - 1) / ((2*n - 1)*(2*n + 1)*(2*n + 3)*(2*n + 5)*(2*n + 7));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__192__1806.03346__Cfraction.tex__202.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 193 *)
s[n_] := (-1)^(n - 1) / ((2*n - 1)*2*n*(2*n + 1)*(2*n + 2)*(2*n + 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__193__1806.03346__Cfraction.tex__272.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 194 *)
s[n_] := (-1)^n / ((2*n + 1) * (2*n + 2) * (2*n + 3) * (2*n + 4) * (2*n + 5));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__194__1806.03346__Cfraction.tex__276.json",
	2,
	200,
	"series"
];

ClearAll[n];

(* 195 *)
s[n_] := Binomial[2 n, n] / ((2 n + 1) * 2^(2 n));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__195__1806.03998__Harmonic.tex__415.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 196 *)
s[k_] := 1 / ((2 k + 1)^2) * (1 / 4^k * Binomial[2 k, k])^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__196__1806.08411__Hyp-FL-Euler.tex__302.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 197 *)
s[n_] := 2*(-1)^n/((2*n + 1)^2) * (1/n + 1/(n + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__197__1806.08411__Hyp-FL-Euler.tex__327.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 198 *)
s[n_] := 8/Pi * ((-1)^n * (Sum[1/(2*k + 1), {k, 0, n}])^2 / (2*n + 1)^2) - 8/Pi * ((-1)^n * Sum[1/(2*k + 1), {k, 0, n}] / (2*n + 1)^3) + 4/Pi * ((-1)^n / (2*n + 1)^4);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__198__1806.08411__Hyp-FL-Euler.tex__353.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 199 *)
s[n_] := 16^n / ((2 n + 1)^3 * Binomial[2 n, n]^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__199__1806.08411__Hyp-FL-Euler.tex__497.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 200 *)
s[n_] := HarmonicNumber[n + 1]/(n + 1) * (1/4^n * Binomial[2*n, n])^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__200__1806.08411__Hyp-FL-Euler.tex__499.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 201 *)
s[k_] := ((2 k + 1) * (2 (k + 1) - 1) / (4 (k + 1)^4)) * (1/4^k Binomial[2 k, k])^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__201__1806.08411__Hyp-FL-Euler.tex__515.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 202 *)
s[n_] := HarmonicNumber[n + 1] / ((n + 1)^2) * (1/4^n * Binomial[2*n, n])^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__202__1806.08411__Hyp-FL-Euler.tex__563.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 203 *)
s[n_] := HarmonicNumber[n + 1, 2]/(n + 1) * (1/4^n * Binomial[2*n, n])^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__203__1806.08411__Hyp-FL-Euler.tex__571.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 204 *)
s[k_] := 1 / (2 k + 1)^3 * (1/4^k * Binomial[2 k, k])^2;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__204__1806.08411__Hyp-FL-Euler.tex__753.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 205 *)
s[k_] := Binomial[2 k, k]^3 / 64^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__205__1806.10896__catalan3v3.tex__73.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 206 *)
s[k_] := (1/2)^3 * (42 k + 5) / (64^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__206__1807.07394__rama-meth-proofs-arx-04.tex__50.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 207 *)
s[k_] := (545140134 k + 13591409) * (-1)^k * Factorial[6 k] / (640320^(3 k) * Factorial[3 k] * Factorial[k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__207__1807.10125__Ram_Chud_163.tex__67.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 208 *)
s[k_] := (6 k + 1)/(256^k) * Binomial[2 k, k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__208__1808.03213__dbinom.tex__72.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 209 *)
s[k_] := (4 k^2)/(4 k^2 - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__209__1808.04717__HS.tex__178.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 210 *)
s[k_] := (3 k + 1) * 16^k / ((2 k + 1)^2 * k^3 * Binomial[2 k, k]^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__210__1808.04717__HS.tex__233.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 211 *)
s[k_] := (12 k^2 - 1) * Binomial[2 k, k]^3 / ((2 k - 1)^2 * 256^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__211__1808.04717__HS.tex__233.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 212 *)
s[k_] := k*(4*k - 1)*Binomial[2*k, k]^3 / ((2*k - 1)^2 * (-64)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__212__1808.04717__HS.tex__233.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 213 *)
s[k_] := (4 k - 1) Binomial[2 k, k]^3 / ((2 k - 1)^3 * (-64)^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__213__1808.04717__HS.tex__233.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 214 *)
s[k_] := (-1)^k * (4*k + 1) * Binomial[2*k, k]^3 / 64^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__214__1808.04717__HS.tex__376.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 215 *)
s[n_] := (-1)^n / (2 n + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__215__1812.06643__ManyproofsExpo.tex__435.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 216 *)
s[k_] := (4 k + 1) * (1/2)^k^3 / Factorial[k]^3 * (-1)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__216__1812.11322__q-clausen01q.tex__51.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 217 *)
s[k_] := (1/2)^k^3 / Factorial[k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__217__1812.11322__q-clausen01q.tex__94.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 218 *)
s[k_] := (-1)^k * (4*k + 1) * (1/2)^(k^3) / Factorial[k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__218__1812.11659__q4k.tex__95.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 219 *)
s[k_] := (1/2)^k^3 / Factorial[k]^3 * (6 k + 1) / 4^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__219__1901.07962__truncated.tex__105.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 220 *)
s[k_] := (-1)^k * (4*k + 1) * (1/2)^(k^3) / Factorial[k]^3;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__220__1903.03766__Hamme-new.tex__85.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 221 *)
s[k_] := (2 k/(2 k - 1))*(2 k/(2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__221__1905.11813__main.tex__45.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 222 *)
s[k_] := 1 - 1/(4 k^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__222__1905.11813__main.tex__51.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 223 *)
s[k_] := (4 k^2)/(4 k^2 - 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__223__1905.11813__main.tex__53.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 224 *)
s[j_] := (2 j) (2 j) / ((2 j - 1) (2 j + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__224__1905.11813__main.tex__74.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 225 *)
s[k_] := (2 k)^2 / ((2 k - 1) (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__225__1906.00122__draft5.tex__122.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 226 *)
s[k_] := ((4 k - 1)^3 * (4 k + 3)) / ((4 k - 3) * (4 k + 1)^3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__226__1906.00122__draft5.tex__224.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 227 *)
s[k_] := ((2 k)^2 * (2 k + 3)) / ((2 k - 1) * (2 k + 2)^2);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__227__1906.00122__draft5.tex__326.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 228 *)
s[n_] := Pochhammer[1/2, n] * Pochhammer[1/4, n] * Pochhammer[3/4, n] * (40 n + 3) / (Factorial[n]^3 * 7^(4 n));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__228__1906.07384__hgm-asai-021920.tex__1145.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 229 *)
s[n_] := (1/2)^n^7 / Factorial[n]^7 * (168 n^3 + 76 n^2 + 14 n + 1) / 2^(6 n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__229__1906.07384__hgm-asai-021920.tex__1160.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 230 *)
s[n_] := (1/2)^n^7 * (1/4)^n * (3/4)^n / Factorial[n]^9 * (43680 n^4 + 20632 n^3 + 4340 n^2 + 466 n + 21) / 2^(12 n);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__230__1906.07384__hgm-asai-021920.tex__1170.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 231 *)
s[k_] := Binomial[2 k, k]^2 / ((2 k + 1) * 16^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__231__1906.08741__BMHS.tex__240.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 232 *)
s[k_] := 1/16^k * (4/(8*k + 1) - 2/(8*k + 4) - 1/(8*k + 5) - 1/(8*k + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__232__1906.09629__BBP33.tex__204.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 233 *)
s[k_] := (-1)^k / 2^(10 k) * (-2^5 / (4 k + 1) - 1 / (4 k + 3) + 2^8 / (10 k + 1) - 2^6 / (10 k + 3) - 2^2 / (10 k + 5) - 2^2 / (10 k + 7) + 1 / (10 k + 9));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__233__1906.09629__BBP33.tex__223.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 234 *)
s[k_] := (-1)^k * Factorial[6 k] * (545140134 k + 13591409) / (Factorial[3 k] * Factorial[k]^3 * 640320^(3 k + 3/2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__234__1906.09629__BBP33.tex__257.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 235 *)
s[k_] := 1/16^k * (2/(8*k + 1) + 2/(8*k + 2) + 1/(8*k + 3) - 1/2/(8*k + 5) - 1/2/(8*k + 6) - 1/4/(8*k + 7));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__235__1906.09629__BBP33.tex__361.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 236 *)
s[k_] := 1/(4*k + 1) - 1/(4*k + 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__236__1906.09629__BBP33.tex__361.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 237 *)
s[k_] := 1/16^k * (2/(8*k) + 1/(8*k + 2) + 1/2/(8*k + 4) + 1/4/(8*k + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__237__1906.09629__BBP33.tex__361.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 238 *)
s[k_] := (-1)^k / (2 k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__238__1906.09629__BBP33.tex__852.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 239 *)
s[k_] := 1/(4*k + 1) - 1/(4*k + 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__239__1906.09629__BBP33.tex__883.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 240 *)
s[j_] := (-1)^j / ((2*j + 2)*(2*j + 3)) + (-1)^j / ((2*j + 1)*(2*j + 2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__240__1906.09629__BBP33.tex__890.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 241 *)
s[k_] := 1/(4*k + 1) - 1/(4*k + 3) - 1/(4*k + 3) + 1/(4*k + 5);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__241__1906.09629__BBP33.tex__890.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 242 *)
s[j_] := (-1)^j * (1/(2*j + 1) - 1/(2*j + 3));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__242__1906.09629__BBP33.tex__890.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 243 *)
s[j_] := (-1)^j * (1/(2*j + 2) - 1/(2*j + 3) + 1/(2*j + 1) - 1/(2*j + 2));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__243__1906.09629__BBP33.tex__890.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 244 *)
s[k_] := 1/(4*k + 1) - 1/(4*k + 3);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__244__1906.09629__BBP33.tex__890.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 245 *)
s[k_] := 1/16^k * (4/(8*k + 1) - 2/(8*k + 4) - 1/(8*k + 5) - 1/(8*k + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__245__1906.09629__BBP33.tex__910.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 246 *)
s[k_] := 1/16^k * (2/(8*k + 1) + 2/(8*k + 2) + 1/(8*k + 3) - 1/2/(8*k + 5) - 1/2/(8*k + 6) - 1/4/(8*k + 7));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__246__1906.09629__BBP33.tex__928.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 247 *)
s[k_] := 1/16^k * (4/(8*k + 1) - 2/(8*k + 4) - 1/(8*k + 5) - 1/(8*k + 6));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__247__1906.09629__BBP33.tex__952.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 248 *)
s[k_] := (-1)^k / (2*k + 1);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__248__1907.04089__Paper1.tex__47.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 249 *)
s[k_] := (2 k)^2 / ((2 k - 1) (2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__249__1907.08984__xi_coefficients.tex__417.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 250 *)
s[k_] := (2 k/(2 k - 1))*(2 k/(2 k + 1));
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__250__1907.12095__probabilistic_wallis.tex__24.json",
	1,
	200,
	"product"
];

ClearAll[n];

(* 251 *)
s[k_] := (1/2)^3 * (6 k + 1) * (1/4)^k;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__251__1908.05123__bilater-p-14-08-19.tex__311.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 252 *)
s[n_] := ((1/2)^n)^3 / (1^n)^3 * (42 n + 5) * (1/64)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__252__1908.05123__bilater-p-14-08-19.tex__355.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 253 *)
s[n_] := Pochhammer[1/2, n] * Pochhammer[1/4, n] * Pochhammer[3/4, n] / Pochhammer[1, n]^5 * (20 n + 3) * (-1/4)^n;
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__253__1908.05123__bilater-p-14-08-19.tex__389.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 254 *)
s[k_] := (3 HarmonicNumber[k, 2] - 1/k^2) / (k^5 Binomial[2 k, k]);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__254__1908.06631__proofofzeta7conjectures.tex__245.json",
	1,
	200,
	"series"
];

ClearAll[n];

(* 255 *)
s[k_] := (-1)^k * Sum[Binomial[2*k - 2*i, k - i]^2 * Binomial[2*i, i]^2 * k * (-1/32)^k, {i, 0, k}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__255__1909.07350__CGG.tex__2204.json",
	0,
	200,
	"series"
];

ClearAll[n];

(* 256 *)
s[k_] := (6 k + 1) * (Pochhammer[1/2, k]^3) / (Factorial[k]^3 * 4^k);
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/recurrences_0-154047/recurrence__256__1909.10294__truncated-2d.tex__98.json",
	0,
	200,
	"series"
];

ClearAll[n];


*)
