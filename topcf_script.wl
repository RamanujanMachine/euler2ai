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


s[n_] := (-1)^n * (3*n + 1) / 32^n * Sum[Binomial[2*n - 2*k, n - k] * Binomial[2*k, k] * Binomial[n, k]^2, {k, 0, n}];
ExportToPCF[
	s,
	"C:/Users/totos/Desktop/9 - arXiv_equations_as_recurrences/test_recurrence__0__0704.2438__threevariablemahlermeasures.tex__203.json",
	0,
	200,
	"series"
]


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



