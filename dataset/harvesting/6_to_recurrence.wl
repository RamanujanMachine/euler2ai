(* ::Package:: *)

(*
This Mathematica file reads the first 200 evaluations of formulas
from files produced by 6_to_recurrence.py
(!!! make sure USE_GUESS == True when 6_to_recurrence.py is run !!!),
and uses them to find the polynomial recurrences for the formulas.
Results are saved as strings in new json files
(which are read by the script 7_merge.py).
*)


baseDir = "C:/Users/totos/Desktop/Refactor";
GuessPath = "C:/Users/totos/Desktop/RISCErgoSum/riscergosum-1.2.3/RISC/Guess.m";
(*
path to Guess should end with 'RISCErgoSum/riscergosum-1.2.3/RISC/Guess.m' (change according to downloaded version)
*)
Get[GuessPath];


baseInput = FileNameJoin[{baseDir, "6_to_recurrence-GUESS"}];               (* Formula evaluations directory *)
baseOutput = FileNameJoin[{baseDir, "6_to_recurrence-GUESS-recurrences"}]; (* Recurrence output directory *)



processJsonFile[jsonFile_, outputDir_] := 
Module[{data, rationalStrings, rationalParts, rationalNumbers, result, outputData, outputFile},
  
  (* Determine output file path *)
  outputFile = FileNameJoin[{outputDir, FileNameTake[jsonFile]}];
  
  (* Check if output file already exists *)
  If[FileExistsQ[outputFile], Return[]];
  
  (* Import JSON data *)
  data = Import[jsonFile, "RawJSON"];
  
  (* Check if "values" key exists *)
  If[KeyExistsQ[data, "values"],
    
    (* Process the rational numbers *)
    rationalStrings = StringTrim[data["values"], {"[", "]"}];
    rationalParts = StringSplit[rationalStrings, ","];
    rationalNumbers = ToExpression /@ rationalParts;
    
    (* Apply GuessMinRE function *)
    result = GuessMinRE[rationalNumbers, f[n]];
    
    (* Prepare output JSON *)
    outputData = <|"recurrence" -> ToString[result, InputForm]|>;
    outputFile = FileNameJoin[{outputDir, FileNameTake[jsonFile]}];
    
    (* Export the processed result *)
    Export[outputFile, outputData, "RawJSON"]
  ];
];


processJsonFiles[baseInput, baseOutput] := Module[{subdirs, jsonFiles, inputSubdir, outputSubdir},
  subdirs = Select[FileNames["*", baseInput], DirectoryQ];
  
  Do[
    outputSubdir = FileNameJoin[{baseOutput, FileNameTake[subdir]}];
    If[! DirectoryQ[outputSubdir], CreateDirectory[outputSubdir]];
    
    jsonFiles = FileNames["*.json", subdir];
    
    Do[processJsonFile[jsonFile, outputSubdir], {jsonFile, jsonFiles}]
  , {subdir, subdirs}]
];



processJsonFiles[baseInput, baseOutput];
