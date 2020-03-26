//Maya ASCII 2015 scene
//Name: Swoosh.ma
//Last modified: Tue, Jun 23, 2015 11:13:29 AM
//Codeset: UTF-8
requires maya "2015";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2015";
fileInfo "version" "2015";
fileInfo "cutIdentifier" "201405190330-916664";
fileInfo "osv" "Mac OS X 10.9.3";
createNode transform -n "rig_all_GRP";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode transform -n "swoosh_CTL" -p "rig_all_GRP";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	addAttr -ci true -k true -sn "character_name" -ln "character_name" -nn "Character Name" 
		-dt "string";
	addAttr -ci true -k true -sn "cc_version" -ln "cc_version" -nn "CC Version" -dt "string";
	addAttr -ci true -k true -sn "rig_version" -ln "rig_version" -nn "Rig Version" -dt "string";
	addAttr -ci true -k true -sn "website" -ln "website" -nn "Website" -dt "string";
	setAttr -l on -k off ".v";
	setAttr -k off ".sx";
	setAttr -k off ".sz";
	setAttr ".mnsl" -type "double3" -1 0.01 -1 ;
	setAttr ".msye" yes;
	setAttr ".aal" -type "attributeAlias" {"Size","scaleY"} ;
	setAttr -l on -k on ".character_name" -type "string" "Swoosh";
	setAttr -l on -k on ".cc_version" -type "string" "1.0";
	setAttr -l on -k on ".rig_version" -type "string" "1.0";
	setAttr -l on -k on ".website" -type "string" "www.animationcreation.net";
createNode nurbsCurve -n "swoosh_CTLShape" -p "swoosh_CTL";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 16;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		1.6636616256048755 1.0186989423306437e-16 -1.6636616256048713
		-2.6842324817655506e-16 1.4406578602191252e-16 -2.3527728341300782
		-1.6636616256048731 1.0186989423306445e-16 -1.6636616256048731
		-2.3527728341300782 3.8459164338472829e-32 -6.2255243878955682e-16
		-1.663661625604874 -1.0186989423306441e-16 1.6636616256048715
		-7.0893637191646628e-16 -1.4406578602191254e-16 2.3527728341300786
		1.6636616256048713 -1.0186989423306445e-16 1.663661625604874
		2.3527728341300782 -8.0665510915750088e-32 1.3229011456588247e-15
		1.6636616256048755 1.0186989423306437e-16 -1.6636616256048713
		-2.6842324817655506e-16 1.4406578602191252e-16 -2.3527728341300782
		-1.6636616256048731 1.0186989423306445e-16 -1.6636616256048731
		;
createNode transform -n "main_all_GRP" -p "rig_all_GRP";
createNode transform -n "main_CTL" -p "main_all_GRP";
	setAttr -l on -k off ".v";
	setAttr ".ro" 3;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "main_CTLShape" -p "main_CTL";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 22;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		1.2650232509454744 7.7460333755867591e-17 -1.2650232509454724
		-2.0410499635957639e-16 1.0954545454349448e-16 -1.7890130382043916
		-1.2650232509454731 7.7460333755867628e-17 -1.2650232509454731
		-1.7890130382043916 3.1743532115818944e-32 -5.1841122089928334e-16
		-1.2650232509454735 -7.7460333755867616e-17 1.2650232509454729
		-5.3906454300115968e-16 -1.0954545454349451e-16 1.7890130382043921
		1.2650232509454724 -7.7460333755867641e-17 1.2650232509454733
		1.7890130382043916 -5.8837077329404669e-32 9.6088239270897271e-16
		1.2650232509454744 7.7460333755867591e-17 -1.2650232509454724
		-2.0410499635957639e-16 1.0954545454349448e-16 -1.7890130382043916
		-1.2650232509454731 7.7460333755867628e-17 -1.2650232509454731
		;
createNode transform -n "main_control_GRP" -p "main_all_GRP";
createNode transform -n "spine_control_joint_GRP" -p "main_control_GRP";
createNode transform -n "top_control_GRP" -p "spine_control_joint_GRP";
	setAttr ".t" -type "double3" 0 4 0 ;
createNode joint -n "top_control_JNT" -p "top_control_GRP";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".v" no;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 4 0 1;
	setAttr ".radi" 0.5;
createNode parentConstraint -n "top_parent_CST" -p "top_control_JNT";
	addAttr -ci true -k true -sn "w1" -ln "torso_IK_CTLW1" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w1";
createNode transform -n "middle_control_GRP" -p "spine_control_joint_GRP";
createNode joint -n "middle_control_JNT" -p "middle_control_GRP";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".v" no;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 2 0 1;
	setAttr ".radi" 0.5;
createNode parentConstraint -n "middle_parent_CST" -p "middle_control_JNT";
	addAttr -ci true -k true -sn "w1" -ln "middle_IK_CTLW1" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w1";
createNode transform -n "bottom_control_GRP" -p "spine_control_joint_GRP";
	setAttr ".t" -type "double3" 0 -4 0 ;
createNode joint -n "bottom_control_JNT" -p "bottom_control_GRP";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".v" no;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".radi" 0.5;
createNode parentConstraint -n "bottom_parent_CST" -p "bottom_control_JNT";
	addAttr -ci true -k true -sn "w1" -ln "hip_IK_CTLW1" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w1";
createNode transform -n "spline_bind_joint_GRP" -p "main_control_GRP";
	setAttr ".v" no;
createNode transform -n "spline_ribbon_GEO" -p "spline_bind_joint_GRP";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 2 0 ;
	setAttr ".sp" -type "double3" 0 2 0 ;
	setAttr ".it" no;
createNode nurbsSurface -n "spline_ribbon_GEOShape" -p "spline_ribbon_GEO";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".tw" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode nurbsSurface -n "spline_ribbon_GEOShapeOrig" -p "spline_ribbon_GEO";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		1 3 0 0 no 
		2 0 1
		11 0 0 0 0.16666666666666666 0.33333333333333331 0.5 0.66666666666666663 0.83333333333333337
		 1 1 1
		
		18
		-0.10000000000000002 0 0
		-0.10000000000000003 0.22222222222222221 0
		-0.10000000000000003 0.66666666666666663 0
		-0.10000000000000003 1.3333333333333333 0
		-0.10000000000000003 2 0
		-0.10000000000000003 2.666666666666667 0
		-0.10000000000000003 3.3333333333333335 0
		-0.10000000000000003 3.7777777777777777 0
		-0.10000000000000002 4 0
		0.10000000000000002 0 0
		0.10000000000000003 0.22222222222222221 0
		0.10000000000000003 0.66666666666666663 0
		0.10000000000000003 1.3333333333333333 0
		0.10000000000000003 2 0
		0.10000000000000003 2.666666666666667 0
		0.10000000000000003 3.3333333333333335 0
		0.10000000000000003 3.7777777777777777 0
		0.10000000000000002 4 0
		
		;
createNode transform -n "spline_01_FOL" -p "spline_bind_joint_GRP";
	setAttr -l on ".it" no;
createNode follicle -n "spline_01_FOLShape" -p "spline_01_FOL";
	setAttr -k off ".v";
	setAttr ".pu" 0.5;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "spline_01_BND" -p "spline_01_FOL";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4 0 1;
	setAttr ".radi" 0.25;
createNode transform -n "spline_02_FOL" -p "spline_bind_joint_GRP";
	setAttr -l on ".it" no;
createNode follicle -n "spline_02_FOLShape" -p "spline_02_FOL";
	setAttr -k off ".v";
	setAttr ".pu" 0.5;
	setAttr ".pv" 0.25;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "spline_02_BND" -p "spline_02_FOL";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999994039535522 0 0 0 0 0.99999994039535522 0 0
		 0 0 1 0 0 -2.125 0 1;
	setAttr ".radi" 0.25;
createNode transform -n "spline_03_FOL" -p "spline_bind_joint_GRP";
	setAttr -l on ".it" no;
createNode follicle -n "spline_03_FOLShape" -p "spline_03_FOL";
	setAttr -k off ".v";
	setAttr ".pu" 0.5;
	setAttr ".pv" 0.5;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "spline_03_BND" -p "spline_03_FOL";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 2.2204460492503131e-16 0 1;
	setAttr ".radi" 0.25;
createNode transform -n "spline_04_FOL" -p "spline_bind_joint_GRP";
	setAttr -l on ".it" no;
createNode follicle -n "spline_04_FOLShape" -p "spline_04_FOL";
	setAttr -k off ".v";
	setAttr ".pu" 0.5;
	setAttr ".pv" 0.75;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "spline_04_BND" -p "spline_04_FOL";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999994039535522 0 0 0 0 0.99999994039535522 0 0
		 0 0 1 0 0 2.125 0 1;
	setAttr ".radi" 0.25;
createNode transform -n "spline_05_FOL" -p "spline_bind_joint_GRP";
	setAttr -l on ".it" no;
createNode follicle -n "spline_05_FOLShape" -p "spline_05_FOL";
	setAttr -k off ".v";
	setAttr ".pu" 0.5;
	setAttr ".pv" 1;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "spline_05_BND" -p "spline_05_FOL";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 4 0 1;
	setAttr ".radi" 0.25;
createNode transform -n "spline_IK_GRP" -p "main_control_GRP";
createNode transform -n "top_IK_GRP" -p "spline_IK_GRP";
	setAttr ".t" -type "double3" 0 4 0 ;
createNode transform -n "top_CTL" -p "top_IK_GRP";
	addAttr -ci true -sn "transparency" -ln "transparency" -dv 1 -min 0 -max 1 -at "double";
	setAttr -l on -k off ".v";
	setAttr ".ro" 3;
	setAttr -k on ".transparency" 0;
createNode nurbsCurve -n "top_CTLShape" -p "top_CTL";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.89521222318440929 5.4815939184018606e-17 -0.89521222318440707
		-1.4443788872460617e-16 7.7521444628257778e-17 -1.2660212672295597
		-0.8952122231844073 5.4815939184018618e-17 -0.8952122231844073
		-1.2660212672295597 2.2463775219853915e-32 -3.6632205308904562e-16
		-0.89521222318440752 -5.4815939184018618e-17 0.89521222318440719
		-3.8147691563714683e-16 -7.752144462825779e-17 1.2660212672295597
		0.89521222318440707 -5.4815939184018618e-17 0.8952122231844073
		1.2660212672295597 -4.1636919133591149e-32 6.805217291030859e-16
		0.89521222318440929 5.4815939184018606e-17 -0.89521222318440707
		-1.4443788872460617e-16 7.7521444628257778e-17 -1.2660212672295597
		-0.8952122231844073 5.4815939184018618e-17 -0.8952122231844073
		;
createNode transform -n "middle_IK_GRP" -p "spline_IK_GRP";
createNode transform -n "middle_IK_CTL" -p "middle_IK_GRP";
	addAttr -ci true -sn "transparency" -ln "transparency" -dv 1 -min 0 -max 1 -at "double";
	setAttr -l on -k off ".v";
	setAttr ".ro" 3;
	setAttr -k on ".transparency" 0;
createNode nurbsCurve -n "middle_IK_CTLShape" -p "middle_IK_CTL";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.89521222318440929 5.4815939184018606e-17 -0.89521222318440707
		-1.4443788872460617e-16 7.7521444628257778e-17 -1.2660212672295597
		-0.8952122231844073 5.4815939184018618e-17 -0.8952122231844073
		-1.2660212672295597 2.2463775219853915e-32 -3.6686128989181337e-16
		-0.89521222318440752 -5.4815939184018618e-17 0.89521222318440719
		-3.8147691563714683e-16 -7.752144462825779e-17 1.2660212672295597
		0.89521222318440707 -5.4815939184018618e-17 0.8952122231844073
		1.2660212672295597 -4.1636919133591149e-32 6.799824923003183e-16
		0.89521222318440929 5.4815939184018606e-17 -0.89521222318440707
		-1.4443788872460617e-16 7.7521444628257778e-17 -1.2660212672295597
		-0.8952122231844073 5.4815939184018618e-17 -0.8952122231844073
		;
createNode parentConstraint -n "middle_IK_GRP_parent_CST" -p "middle_IK_GRP";
	addAttr -ci true -k true -sn "w0" -ln "torso_control_JNTW0" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "w1" -ln "hip_control_JNTW1" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "w2" -ln "middle_IK_damper_GRPW2" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 3 ".tg";
	setAttr ".tg[0].tot" -type "double3" 0 -4 0 ;
	setAttr ".tg[1].tot" -type "double3" 0 4 0 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
	setAttr -k on ".w2";
createNode orientConstraint -n "middle_IK_GRP_orient_CST" -p "middle_IK_GRP";
	addAttr -ci true -k true -sn "w0" -ln "torso_IK_CTLW0" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "w1" -ln "hip_IK_CTLW1" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr -k on ".w0";
	setAttr -k on ".w1";
createNode transform -n "middle_IK_damper_GRP" -p "spline_IK_GRP";
createNode pointConstraint -n "middle_IK_damper_GRP_point_CST" -p "middle_IK_damper_GRP";
	addAttr -ci true -k true -sn "w0" -ln "torso_IK_CTLW0" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "w1" -ln "hip_IK_CTLW1" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr -k on ".w0";
	setAttr -k on ".w1";
createNode transform -n "bottom_IK_GRP" -p "spline_IK_GRP";
	setAttr ".t" -type "double3" 0 -4 0 ;
createNode transform -n "bottom_CTL" -p "bottom_IK_GRP";
	addAttr -ci true -sn "transparency" -ln "transparency" -dv 1 -min 0 -max 1 -at "double";
	setAttr -l on -k off ".v";
	setAttr ".ro" 3;
	setAttr -k on ".transparency" 0;
createNode nurbsCurve -n "bottom_CTLShape" -p "bottom_CTL";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.89521222318440929 5.4815939184018606e-17 -0.89521222318440707
		-1.4443788872460617e-16 7.7521444628257778e-17 -1.2660212672295597
		-0.8952122231844073 5.4815939184018618e-17 -0.8952122231844073
		-1.2660212672295597 2.2463775219853915e-32 -3.6686128989181337e-16
		-0.89521222318440752 -5.4815939184018618e-17 0.89521222318440719
		-3.8147691563714683e-16 -7.752144462825779e-17 1.2660212672295597
		0.89521222318440707 -5.4815939184018618e-17 0.8952122231844073
		1.2660212672295597 -4.1636919133591149e-32 6.799824923003183e-16
		0.89521222318440929 5.4815939184018606e-17 -0.89521222318440707
		-1.4443788872460617e-16 7.7521444628257778e-17 -1.2660212672295597
		-0.8952122231844073 5.4815939184018618e-17 -0.8952122231844073
		;
createNode transform -n "swoosh_GEO" -p "rig_all_GRP";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode mesh -n "swoosh_GEOShape" -p "swoosh_GEO";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.49878114461898804 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".sdt" 0;
	setAttr ".ugsdt" no;
	setAttr ".dr" 3;
	setAttr ".dsm" 2;
	setAttr ".vcs" 2;
createNode mesh -n "swoosh_GEOShape1Orig" -p "swoosh_GEO";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 107 ".uvst[0].uvsp[0:106]" -type "float2" 0.875 0.058880121
		 1 0.058880121 0.12499994 0.058880121 0.24999997 0.058880121 0.375 0.058880121 0.5
		 0.058880121 0.625 0.058880121 0.75 0.058880121 0.625 0.033652842 0.375 0.033652842
		 0.12499994 0.033652842 0.875 0.96390945 0.12499994 0.96390945 0.375 0.96390945 0.625
		 0.96390945 0.875 0.033652842 0 0.058880121 0.875 0.14686039 0 0.14686039 0.12499994
		 0.14686039 0.24999997 0.14686039 0.375 0.14686039 0.5 0.14686039 0.625 0.14686039
		 0.75 0.14686039 1 0.14686039 0.875 0.23484069 0 0.23484069 0.12499994 0.23484069
		 0.24999997 0.23484069 0.375 0.23484069 0.5 0.23484069 0.625 0.23484069 0.75 0.23484069
		 1 0.23484069 0.875 0.3228209 0 0.3228209 0.12499994 0.3228209 0.24999997 0.3228209
		 0.375 0.3228209 0.5 0.3228209 0.625 0.3228209 0.75 0.3228209 1 0.3228209 0.875 0.4108012
		 0 0.4108012 0.12499994 0.4108012 0.24999997 0.4108012 0.375 0.4108012 0.5 0.4108012
		 0.625 0.4108012 0.75 0.4108012 1 0.4108012 0.875 0.49878135 0 0.49878135 0.12499994
		 0.49878135 0.24999997 0.49878135 0.375 0.49878135 0.5 0.49878135 0.625 0.49878135
		 0.75 0.49878135 1 0.49878135 0.875 0.58676159 0 0.58676159 0.12499994 0.58676159
		 0.24999997 0.58676159 0.375 0.58676159 0.5 0.58676159 0.625 0.58676159 0.75 0.58676159
		 1 0.58676159 0.875 0.67474174 0 0.67474174 0.12499994 0.67474174 0.24999997 0.67474174
		 0.375 0.67474174 0.5 0.67474174 0.625 0.67474174 0.75 0.67474174 1 0.67474174 0.875
		 0.76272202 0 0.76272202 0.12499994 0.76272202 0.24999997 0.76272202 0.375 0.76272202
		 0.5 0.76272202 0.625 0.76272202 0.75 0.76272202 1 0.76272202 0.875 0.85070217 0 0.85070217
		 0.12499994 0.85070217 0.24999997 0.85070217 0.375 0.85070217 0.5 0.85070217 0.625
		 0.85070217 0.75 0.85070217 1 0.9386822 0.875 0.9386822 0 0.9386822 0.12499994 0.9386822
		 0.24999994 0.9386822 0.375 0.9386822 0.5 0.9386822 0.625 0.9386822 0.75 0.9386822
		 1 0.85070217;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".sdt" 0;
	setAttr ".ugsdt" no;
	setAttr -s 90 ".vt[0:89]"  0.70710671 -5 -0.70710671 0 -5 -0.99999988
		 -0.70710671 -5 -0.70710671 -0.99999988 -5 0 -0.70710671 -5 0.70710671 0 -5 0.99999994
		 0.70710677 -5 0.70710677 1 -5 0 0.70710671 -4 -0.70710671 0 -4 -0.99999988 -0.70710671 -4 -0.70710671
		 -0.99999988 -4 0 -0.70710671 -4 0.70710671 0 -4 0.99999994 0.70710677 -4 0.70710677
		 1 -4 0 0.70710671 -3 -0.70710671 0 -3 -0.99999988 -0.70710671 -3 -0.70710671 -0.99999988 -3 0
		 -0.70710671 -3 0.70710671 0 -3 0.99999994 0.70710677 -3 0.70710677 1 -3 0 0.70710671 -2 -0.70710671
		 0 -2 -0.99999988 -0.70710671 -2 -0.70710671 -0.99999988 -2 0 -0.70710671 -2 0.70710671
		 0 -2 0.99999994 0.70710677 -2 0.70710677 1 -2 0 0.70710671 -1 -0.70710671 0 -1 -0.99999988
		 -0.70710671 -1 -0.70710671 -0.99999988 -1 0 -0.70710671 -1 0.70710671 0 -1 0.99999994
		 0.70710677 -1 0.70710677 1 -1 0 0.70710671 0 -0.70710671 0 0 -0.99999988 -0.70710671 0 -0.70710671
		 -0.99999988 0 0 -0.70710671 0 0.70710671 0 0 0.99999994 0.70710677 0 0.70710677 1 0 0
		 0.70710671 1 -0.70710671 0 1 -0.99999988 -0.70710671 1 -0.70710671 -0.99999988 1 0
		 -0.70710671 1 0.70710671 0 1 0.99999994 0.70710677 1 0.70710677 1 1 0 0.70710671 2 -0.70710671
		 0 2 -0.99999988 -0.70710671 2 -0.70710671 -0.99999988 2 0 -0.70710671 2 0.70710671
		 0 2 0.99999994 0.70710677 2 0.70710677 1 2 0 0.70710671 3 -0.70710671 0 3 -0.99999988
		 -0.70710671 3 -0.70710671 -0.99999988 3 0 -0.70710671 3 0.70710671 0 3 0.99999994
		 0.70710677 3 0.70710677 1 3 0 0.70710671 4 -0.70710671 0 4 -0.99999988 -0.70710671 4 -0.70710671
		 -0.99999988 4 0 -0.70710671 4 0.70710671 0 4 0.99999994 0.70710677 4 0.70710677 1 4 0
		 0.70710671 5 -0.70710671 0 5 -0.99999988 -0.70710671 5 -0.70710671 -0.99999988 5 0
		 -0.70710671 5 0.70710671 0 5 0.99999994 0.70710677 5 0.70710677 1 5 0 0 -5 0 0 5 0;
	setAttr -s 176 ".ed";
	setAttr ".ed[0:165]"  0 1 1 1 2 1 2 3 1 3 4 1 4 5 1 5 6 1 6 7 1 7 0 1 8 9 1
		 9 10 1 10 11 1 11 12 1 12 13 1 13 14 1 14 15 1 15 8 1 16 17 1 17 18 1 18 19 1 19 20 1
		 20 21 1 21 22 1 22 23 1 23 16 1 24 25 1 25 26 1 26 27 1 27 28 1 28 29 1 29 30 1 30 31 1
		 31 24 1 32 33 1 33 34 1 34 35 1 35 36 1 36 37 1 37 38 1 38 39 1 39 32 1 40 41 1 41 42 1
		 42 43 1 43 44 1 44 45 1 45 46 1 46 47 1 47 40 1 48 49 1 49 50 1 50 51 1 51 52 1 52 53 1
		 53 54 1 54 55 1 55 48 1 56 57 1 57 58 1 58 59 1 59 60 1 60 61 1 61 62 1 62 63 1 63 56 1
		 64 65 1 65 66 1 66 67 1 67 68 1 68 69 1 69 70 1 70 71 1 71 64 1 72 73 1 73 74 1 74 75 1
		 75 76 1 76 77 1 77 78 1 78 79 1 79 72 1 80 81 1 81 82 1 82 83 1 83 84 1 84 85 1 85 86 1
		 86 87 1 87 80 1 0 8 0 1 9 0 2 10 0 3 11 0 4 12 0 5 13 0 6 14 0 7 15 0 8 16 0 9 17 0
		 10 18 0 11 19 0 12 20 0 13 21 0 14 22 0 15 23 0 16 24 0 17 25 0 18 26 0 19 27 0 20 28 0
		 21 29 0 22 30 0 23 31 0 24 32 0 25 33 0 26 34 0 27 35 0 28 36 0 29 37 0 30 38 0 31 39 0
		 32 40 0 33 41 0 34 42 0 35 43 0 36 44 0 37 45 0 38 46 0 39 47 0 40 48 0 41 49 0 42 50 0
		 43 51 0 44 52 0 45 53 0 46 54 0 47 55 0 48 56 0 49 57 0 50 58 0 51 59 0 52 60 0 53 61 0
		 54 62 0 55 63 0 56 64 0 57 65 0 58 66 0 59 67 0 60 68 0 61 69 0 62 70 0 63 71 0 64 72 0
		 65 73 0 66 74 0 67 75 0 68 76 0 69 77 0 70 78 0 71 79 0 72 80 0 73 81 0 74 82 0 75 83 0
		 76 84 0 77 85 0;
	setAttr ".ed[166:175]" 78 86 0 79 87 0 88 1 1 88 3 1 88 5 1 88 7 1 81 89 1
		 83 89 1 85 89 1 87 89 1;
	setAttr -s 88 -ch 352 ".fc[0:87]" -type "polyFaces" 
		f 4 0 89 -9 -89
		mu 0 4 0 1 25 17
		f 4 1 90 -10 -90
		mu 0 4 16 2 19 18
		f 4 2 91 -11 -91
		mu 0 4 2 3 20 19
		f 4 3 92 -12 -92
		mu 0 4 3 4 21 20
		f 4 4 93 -13 -93
		mu 0 4 4 5 22 21
		f 4 5 94 -14 -94
		mu 0 4 5 6 23 22
		f 4 6 95 -15 -95
		mu 0 4 6 7 24 23
		f 4 7 88 -16 -96
		mu 0 4 7 0 17 24
		f 4 8 97 -17 -97
		mu 0 4 17 25 34 26
		f 4 9 98 -18 -98
		mu 0 4 18 19 28 27
		f 4 10 99 -19 -99
		mu 0 4 19 20 29 28
		f 4 11 100 -20 -100
		mu 0 4 20 21 30 29
		f 4 12 101 -21 -101
		mu 0 4 21 22 31 30
		f 4 13 102 -22 -102
		mu 0 4 22 23 32 31
		f 4 14 103 -23 -103
		mu 0 4 23 24 33 32
		f 4 15 96 -24 -104
		mu 0 4 24 17 26 33
		f 4 16 105 -25 -105
		mu 0 4 26 34 43 35
		f 4 17 106 -26 -106
		mu 0 4 27 28 37 36
		f 4 18 107 -27 -107
		mu 0 4 28 29 38 37
		f 4 19 108 -28 -108
		mu 0 4 29 30 39 38
		f 4 20 109 -29 -109
		mu 0 4 30 31 40 39
		f 4 21 110 -30 -110
		mu 0 4 31 32 41 40
		f 4 22 111 -31 -111
		mu 0 4 32 33 42 41
		f 4 23 104 -32 -112
		mu 0 4 33 26 35 42
		f 4 24 113 -33 -113
		mu 0 4 35 43 52 44
		f 4 25 114 -34 -114
		mu 0 4 36 37 46 45
		f 4 26 115 -35 -115
		mu 0 4 37 38 47 46
		f 4 27 116 -36 -116
		mu 0 4 38 39 48 47
		f 4 28 117 -37 -117
		mu 0 4 39 40 49 48
		f 4 29 118 -38 -118
		mu 0 4 40 41 50 49
		f 4 30 119 -39 -119
		mu 0 4 41 42 51 50
		f 4 31 112 -40 -120
		mu 0 4 42 35 44 51
		f 4 32 121 -41 -121
		mu 0 4 44 52 61 53
		f 4 33 122 -42 -122
		mu 0 4 45 46 55 54
		f 4 34 123 -43 -123
		mu 0 4 46 47 56 55
		f 4 35 124 -44 -124
		mu 0 4 47 48 57 56
		f 4 36 125 -45 -125
		mu 0 4 48 49 58 57
		f 4 37 126 -46 -126
		mu 0 4 49 50 59 58
		f 4 38 127 -47 -127
		mu 0 4 50 51 60 59
		f 4 39 120 -48 -128
		mu 0 4 51 44 53 60
		f 4 40 129 -49 -129
		mu 0 4 53 61 70 62
		f 4 41 130 -50 -130
		mu 0 4 54 55 64 63
		f 4 42 131 -51 -131
		mu 0 4 55 56 65 64
		f 4 43 132 -52 -132
		mu 0 4 56 57 66 65
		f 4 44 133 -53 -133
		mu 0 4 57 58 67 66
		f 4 45 134 -54 -134
		mu 0 4 58 59 68 67
		f 4 46 135 -55 -135
		mu 0 4 59 60 69 68
		f 4 47 128 -56 -136
		mu 0 4 60 53 62 69
		f 4 48 137 -57 -137
		mu 0 4 62 70 79 71
		f 4 49 138 -58 -138
		mu 0 4 63 64 73 72
		f 4 50 139 -59 -139
		mu 0 4 64 65 74 73
		f 4 51 140 -60 -140
		mu 0 4 65 66 75 74
		f 4 52 141 -61 -141
		mu 0 4 66 67 76 75
		f 4 53 142 -62 -142
		mu 0 4 67 68 77 76
		f 4 54 143 -63 -143
		mu 0 4 68 69 78 77
		f 4 55 136 -64 -144
		mu 0 4 69 62 71 78
		f 4 56 145 -65 -145
		mu 0 4 71 79 88 80
		f 4 57 146 -66 -146
		mu 0 4 72 73 82 81
		f 4 58 147 -67 -147
		mu 0 4 73 74 83 82
		f 4 59 148 -68 -148
		mu 0 4 74 75 84 83
		f 4 60 149 -69 -149
		mu 0 4 75 76 85 84
		f 4 61 150 -70 -150
		mu 0 4 76 77 86 85
		f 4 62 151 -71 -151
		mu 0 4 77 78 87 86
		f 4 63 144 -72 -152
		mu 0 4 78 71 80 87
		f 4 64 153 -73 -153
		mu 0 4 80 88 106 89
		f 4 65 154 -74 -154
		mu 0 4 81 82 91 90
		f 4 66 155 -75 -155
		mu 0 4 82 83 92 91
		f 4 67 156 -76 -156
		mu 0 4 83 84 93 92
		f 4 68 157 -77 -157
		mu 0 4 84 85 94 93
		f 4 69 158 -78 -158
		mu 0 4 85 86 95 94
		f 4 70 159 -79 -159
		mu 0 4 86 87 96 95
		f 4 71 152 -80 -160
		mu 0 4 87 80 89 96
		f 4 72 161 -81 -161
		mu 0 4 89 106 97 98
		f 4 73 162 -82 -162
		mu 0 4 90 91 100 99
		f 4 74 163 -83 -163
		mu 0 4 91 92 101 100
		f 4 75 164 -84 -164
		mu 0 4 92 93 102 101
		f 4 76 165 -85 -165
		mu 0 4 93 94 103 102
		f 4 77 166 -86 -166
		mu 0 4 94 95 104 103
		f 4 78 167 -87 -167
		mu 0 4 95 96 105 104
		f 4 79 160 -88 -168
		mu 0 4 96 89 98 105
		f 4 -2 -169 169 -3
		mu 0 4 2 16 10 3
		f 4 -4 -170 170 -5
		mu 0 4 4 3 9 5
		f 4 -6 -171 171 -7
		mu 0 4 6 5 8 7
		f 4 -8 -172 168 -1
		mu 0 4 0 7 15 1
		f 4 -173 81 82 173
		mu 0 4 12 99 100 101
		f 4 -174 83 84 174
		mu 0 4 13 101 102 103
		f 4 -175 85 86 175
		mu 0 4 14 103 104 105
		f 4 -176 87 80 172
		mu 0 4 11 105 98 97;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".vcs" 2;
createNode groupId -n "spine_ribbon_SKNGroupId";
	setAttr ".ihi" 0;
createNode objectSet -n "spine_ribbon_SKNSet";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "spline_ribbon_SKN";
	setAttr ".skm" 1;
	setAttr -s 18 ".wl";
	setAttr ".wl[0].w[0]"  1;
	setAttr ".wl[1].w[0]"  1;
	setAttr -s 2 ".wl[2].w[0:1]"  0.75 0.25;
	setAttr -s 2 ".wl[3].w[0:1]"  0.375 0.625;
	setAttr -s 3 ".wl[4].w[0:2]"  0.15 0.7 0.15;
	setAttr -s 2 ".wl[5].w[1:2]"  0.625 0.375;
	setAttr -s 2 ".wl[6].w[1:2]"  0.25 0.75;
	setAttr ".wl[7].w[2]"  1;
	setAttr ".wl[8].w[2]"  1;
	setAttr ".wl[9].w[0]"  1;
	setAttr ".wl[10].w[0]"  1;
	setAttr -s 2 ".wl[11].w[0:1]"  0.75 0.25;
	setAttr -s 2 ".wl[12].w[0:1]"  0.375 0.625;
	setAttr -s 3 ".wl[13].w[0:2]"  0.15 0.7 0.15;
	setAttr -s 2 ".wl[14].w[1:2]"  0.625 0.375;
	setAttr -s 2 ".wl[15].w[1:2]"  0.25 0.75;
	setAttr ".wl[16].w[2]"  1;
	setAttr ".wl[17].w[2]"  1;
	setAttr -s 3 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -2 0 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4 0 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 3 ".ma";
	setAttr -s 3 ".dpf[0:2]"  4 4 4;
	setAttr -s 3 ".lw";
	setAttr -s 3 ".lw";
	setAttr ".ucm" yes;
	setAttr -s 3 ".ifcl";
	setAttr -s 3 ".ifcl";
createNode dagPose -n "bindPose1";
	setAttr -s 3 ".wm";
	setAttr -s 3 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr -s 3 ".m";
	setAttr -s 3 ".p";
	setAttr ".bp" yes;
createNode groupParts -n "spine_ribbon_SKNGroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode tweak -n "tweak1";
createNode objectSet -n "tweakSet1";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId2";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts2";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode plusMinusAverage -n "bottom_middle_sns_PMA";
	setAttr ".op" 3;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode plusMinusAverage -n "top_middle_sns_PMA";
	setAttr ".op" 3;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode groupId -n "skinCluster1GroupId";
	setAttr ".ihi" 0;
createNode objectSet -n "skinCluster1Set";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "skinCluster1";
	setAttr -s 90 ".wl";
	setAttr ".wl[0].w[0]"  1;
	setAttr ".wl[1].w[0]"  1;
	setAttr ".wl[2].w[0]"  1;
	setAttr ".wl[3].w[0]"  1;
	setAttr ".wl[4].w[0]"  1;
	setAttr ".wl[5].w[0]"  1;
	setAttr ".wl[6].w[0]"  1;
	setAttr ".wl[7].w[0]"  1;
	setAttr -s 5 ".wl[8].w[0:4]"  0.74381939935649666 0.24868876117040434 
		0.0044921825728032926 0.0013333181352332469 0.0016663387650623918;
	setAttr -s 5 ".wl[9].w[0:4]"  0.74455242564904056 0.24844287097597584 
		0.0042345736046790067 0.0011502182504940122 0.0016199115198105574;
	setAttr -s 5 ".wl[10].w[0:4]"  0.7438193992502794 0.24868876127393491 
		0.0044921826831602635 0.0013333180275629537 0.0016663387650623918;
	setAttr -s 5 ".wl[11].w[0:4]"  0.74455242564904056 0.24844287097597584 
		0.0042345736046790067 0.0011502182504940122 0.0016199115198105574;
	setAttr -s 5 ".wl[12].w[0:4]"  0.74381939935649666 0.24868876117040434 
		0.0044921825728032926 0.0013333181352332469 0.0016663387650623918;
	setAttr -s 5 ".wl[13].w[0:4]"  0.74455242566028335 0.24844287042356603 
		0.0042345739387016296 0.0011502183412230803 0.0016199116362258792;
	setAttr -s 5 ".wl[14].w[0:4]"  0.74381939938475738 0.24868876045376331 
		0.0044921830306968906 0.001333318249304698 0.0016663388814777136;
	setAttr -s 5 ".wl[15].w[0:4]"  0.74455242565722612 0.24844286996406775 
		0.0042345744035521375 0.0011502183389280973 0.0016199116362258792;
	setAttr -s 5 ".wl[16].w[0:4]"  0.49074618629940153 0.45772592826865299 
		0.047674853357300352 0.0027864430451392526 0.0010665890295058489;
	setAttr -s 5 ".wl[17].w[0:4]"  0.49091656242450299 0.45758993189430913 
		0.04766010341091028 0.0027856697289399038 0.0010477325413376093;
	setAttr -s 5 ".wl[18].w[0:4]"  0.49074618632835221 0.45772593146767104 
		0.04767485065340811 0.0027864426374780795 0.0010665889130905271;
	setAttr -s 5 ".wl[19].w[0:4]"  0.49091656242450299 0.45758993189430913 
		0.04766010341091028 0.0027856697289399038 0.0010477325413376093;
	setAttr -s 5 ".wl[20].w[0:4]"  0.49074618629980937 0.45772592847199867 
		0.047674853400326955 0.0027864427983591423 0.0010665890295058489;
	setAttr -s 5 ".wl[21].w[0:4]"  0.49091659222495238 0.4575899020040457 
		0.04766010326067497 0.0027856699689893269 0.0010477325413376093;
	setAttr -s 5 ".wl[22].w[0:4]"  0.49074621607114893 0.45772590155422732 
		0.047674850469755413 0.0027864428753623946 0.0010665890295058489;
	setAttr -s 5 ".wl[23].w[0:4]"  0.49091659222512635 0.45758990207532352 
		0.047660103193842507 0.0027856699643699885 0.0010477325413376093;
	setAttr -s 5 ".wl[24].w[0:4]"  0.2488725536942937 0.51036340565513472 
		0.23088073085014807 0.0089486611236480815 0.00093464867677539587;
	setAttr -s 5 ".wl[25].w[0:4]"  0.2488835528619753 0.5103320646484738 
		0.23089978491849877 0.0089492821837285821 0.00093531538732349873;
	setAttr -s 5 ".wl[26].w[0:4]"  0.2488725387994967 0.5103634158092325 
		0.23088073547000018 0.0089486613027028802 0.00093464861856773496;
	setAttr -s 5 ".wl[27].w[0:4]"  0.2488835528619753 0.5103320646484738 
		0.23089978491849877 0.0089492821837285821 0.00093531538732349873;
	setAttr -s 5 ".wl[28].w[0:4]"  0.2488725536942937 0.51036340565513472 
		0.23088073085014807 0.0089486611236480815 0.00093464867677539587;
	setAttr -s 5 ".wl[29].w[0:4]"  0.24888356779307166 0.51033201549217677 
		0.23089981781290397 0.0089492834563164123 0.00093531544553115964;
	setAttr -s 5 ".wl[30].w[0:4]"  0.24887256856912793 0.5103634003165487 
		0.23088072062923076 0.0089486617501096481 0.00093464873498305678;
	setAttr -s 5 ".wl[31].w[0:4]"  0.24888356780758927 0.51033201553018359 
		0.2308998178206372 0.0089492834542664341 0.00093531538732349873;
	setAttr -s 5 ".wl[32].w[0:4]"  0.08820883889379233 0.3753062257264777 
		0.49063940440813242 0.04162401850120323 0.0042215124703943729;
	setAttr -s 5 ".wl[33].w[0:4]"  0.088213309746773258 0.37530552101475007 
		0.49063694064329183 0.041623799718605956 0.0042204288765788078;
	setAttr -s 5 ".wl[34].w[0:4]"  0.08820883889379233 0.37530622572647765 
		0.49063940440813242 0.041624018501203217 0.0042215124703943729;
	setAttr -s 5 ".wl[35].w[0:4]"  0.088213309746773258 0.37530552101475007 
		0.49063694064329183 0.041623799718605956 0.0042204288765788078;
	setAttr -s 5 ".wl[36].w[0:4]"  0.08820883889379233 0.37530622572647765 
		0.49063940440813242 0.041624018501203217 0.0042215124703943729;
	setAttr -s 5 ".wl[37].w[0:4]"  0.088213317173807676 0.37530551774484805 
		0.4906369368691948 0.041623799335570644 0.0042204288765788078;
	setAttr -s 5 ".wl[38].w[0:4]"  0.088208838914590623 0.37530623334839058 
		0.49063938935870316 0.041624025907921296 0.0042215124703943729;
	setAttr -s 5 ".wl[39].w[0:4]"  0.088213317172896433 0.37530551754662161 
		0.49063693711069922 0.041623799293203936 0.0042204288765788078;
	setAttr -s 5 ".wl[40].w[0:4]"  0.02263840856494934 0.16651251119808716 
		0.6214581760800445 0.16490056075012247 0.024490343406796455;
	setAttr -s 5 ".wl[41].w[0:4]"  0.022638369757938533 0.16651252473890682 
		0.62145820436955568 0.16490056331473801 0.024490337818861008;
	setAttr -s 5 ".wl[42].w[0:4]"  0.02263840856494934 0.16651251119808716 
		0.6214581760800445 0.16490056075012247 0.024490343406796455;
	setAttr -s 5 ".wl[43].w[0:4]"  0.022638369757938533 0.16651252473890682 
		0.62145820436955568 0.16490056331473801 0.024490337818861008;
	setAttr -s 5 ".wl[44].w[0:4]"  0.02263840856494934 0.16651251119808716 
		0.6214581760800445 0.16490056075012247 0.024490343406796455;
	setAttr -s 5 ".wl[45].w[0:4]"  0.022638369757938533 0.16651252473890682 
		0.62145820436955568 0.16490056331473801 0.024490337818861008;
	setAttr -s 5 ".wl[46].w[0:4]"  0.02263841224937781 0.16651252531828967 
		0.62145816191331738 0.16490055711221865 0.024490343406796455;
	setAttr -s 5 ".wl[47].w[0:4]"  0.022638369757938533 0.16651252473890682 
		0.62145820436955568 0.16490056331473801 0.024490337818861008;
	setAttr -s 5 ".wl[48].w[0:4]"  0.0040031565229690516 0.039893031252795884 
		0.49175053651185024 0.36858310293759317 0.095770172774791718;
	setAttr -s 5 ".wl[49].w[0:4]"  0.0040031582070540394 0.039892949088390785 
		0.49174810756600906 0.36858150709384557 0.095774278044700623;
	setAttr -s 5 ".wl[50].w[0:4]"  0.0040031565229690516 0.039893031252795884 
		0.49175053651185024 0.36858310293759317 0.095770172774791718;
	setAttr -s 5 ".wl[51].w[0:4]"  0.0040031582070540394 0.039892949088390785 
		0.49174810756600906 0.36858150709384557 0.095774278044700623;
	setAttr -s 5 ".wl[52].w[0:4]"  0.0040031565229690516 0.039893031252795884 
		0.49175053651185024 0.36858310293759317 0.095770172774791718;
	setAttr -s 5 ".wl[53].w[0:4]"  0.0040031582032952285 0.039892952670505119 
		0.49174810520716761 0.36858150587433142 0.095774278044700623;
	setAttr -s 5 ".wl[54].w[0:4]"  0.0040031565193545454 0.03989303121614151 
		0.49175053609233887 0.36858310339737338 0.095770172774791718;
	setAttr -s 5 ".wl[55].w[0:4]"  0.0040031582007462128 0.039892952644654381 
		0.49174810490987891 0.36858150620001984 0.095774278044700623;
	setAttr -s 5 ".wl[56].w[0:4]"  0.00091370299359211208 0.0085693472581948333 
		0.22638794022345582 0.49917107490676099 0.26495793461799622;
	setAttr -s 5 ".wl[57].w[0:4]"  0.00090796441361880363 0.0085690369209535759 
		0.22640432148215722 0.49913773517239091 0.26498094201087952;
	setAttr -s 5 ".wl[58].w[0:4]"  0.00091370293684734218 0.0085693472588572045 
		0.22638794024095454 0.49917107494534468 0.26495793461799622;
	setAttr -s 5 ".wl[59].w[0:4]"  0.00090796441361880363 0.0085690369209535759 
		0.22640432148215722 0.49913773517239091 0.26498094201087952;
	setAttr -s 5 ".wl[60].w[0:4]"  0.00091370293684734218 0.0085693472588572045 
		0.22638794024095454 0.49917107494534468 0.26495793461799622;
	setAttr -s 5 ".wl[61].w[0:4]"  0.00090796441325755668 0.0085690378256292228 
		0.2264043211229019 0.4991377346273318 0.26498094201087952;
	setAttr -s 5 ".wl[62].w[0:4]"  0.00091370299320816389 0.0085693481626760108 
		0.2263879398250577 0.49917107440106195 0.26495793461799622;
	setAttr -s 5 ".wl[63].w[0:4]"  0.00090796441315934 0.0085690378252293864 
		0.22640432102461994 0.49913773472611178 0.26498094201087952;
	setAttr -s 5 ".wl[64].w[0:4]"  0.00094654511355585463 0.0027893054902878053 
		0.046195997641125752 0.4395792243906812 0.51048892736434937;
	setAttr -s 5 ".wl[65].w[0:4]"  0.00092971108043151589 0.002789565112887984 
		0.046189280125522356 0.43945898833218966 0.51063245534896851;
	setAttr -s 5 ".wl[66].w[0:4]"  0.00094654511360735695 0.0027893054902732341 
		0.046195997643284366 0.43957922438848568 0.51048892736434937;
	setAttr -s 5 ".wl[67].w[0:4]"  0.00092971108043151589 0.002789565112887984 
		0.046189280125522356 0.43945898833218966 0.51063245534896851;
	setAttr -s 5 ".wl[68].w[0:4]"  0.00094654511360735695 0.0027893054902732341 
		0.046195997643284373 0.43957922438848568 0.51048892736434937;
	setAttr -s 5 ".wl[69].w[0:4]"  0.00092971108014434944 0.0027895653464822361 
		0.046189280019778282 0.43945898820462664 0.51063245534896851;
	setAttr -s 5 ".wl[70].w[0:4]"  0.00094654510590906529 0.0027893057021989381 
		0.046196000943181478 0.43957922088436113 0.51048892736434937;
	setAttr -s 5 ".wl[71].w[0:4]"  0.00092971108008220687 0.0027895653462956358 
		0.046189279938417295 0.43945898828623636 0.51063245534896851;
	setAttr -s 5 ".wl[72].w[0:4]"  0.0017317491136848362 0.0013533051806991802 
		0.0043594416127984686 0.23597682023966809 0.75657868385314941;
	setAttr -s 5 ".wl[73].w[0:4]"  0.0016016030268961223 0.0011676524683510512 
		0.00409764580590614 0.23569277010082423 0.75744032859802246;
	setAttr -s 5 ".wl[74].w[0:4]"  0.0017317491136848362 0.0013533051806991802 
		0.0043594416127984686 0.23597682023966809 0.75657868385314941;
	setAttr -s 5 ".wl[75].w[0:4]"  0.0016016030268961223 0.0011676524683510512 
		0.00409764580590614 0.23569277010082423 0.75744032859802246;
	setAttr -s 5 ".wl[76].w[0:4]"  0.0017317491136848362 0.0013533051806991802 
		0.0043594416127984686 0.23597682023966809 0.75657868385314941;
	setAttr -s 5 ".wl[77].w[0:4]"  0.001601603023759141 0.0011676524660630737 
		0.0040976462731635464 0.23569276963899177 0.75744032859802246;
	setAttr -s 5 ".wl[78].w[0:4]"  0.0017317491096500645 0.0013533052976403123 
		0.0043594420774516881 0.23597681966210851 0.75657868385314941;
	setAttr -s 5 ".wl[79].w[0:4]"  0.0016016030231518663 0.0011676525857161404 
		0.0040976462709991831 0.23569276952211035 0.75744032859802246;
	setAttr ".wl[80].w[4]"  1;
	setAttr ".wl[81].w[4]"  1;
	setAttr ".wl[82].w[4]"  1;
	setAttr ".wl[83].w[4]"  1;
	setAttr ".wl[84].w[4]"  1;
	setAttr ".wl[85].w[4]"  1;
	setAttr ".wl[86].w[4]"  1;
	setAttr ".wl[87].w[4]"  1;
	setAttr ".wl[88].w[0]"  1;
	setAttr ".wl[89].w[4]"  1;
	setAttr -s 5 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 4 0 1;
	setAttr ".pm[1]" -type "matrix" 1.0000000596046483 0 0 0 0 1.0000000596046483 0 0
		 0 0 1 0 0 2.1250001266598777 0 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -2.2204460492503131e-16 0 1;
	setAttr ".pm[3]" -type "matrix" 1.0000000596046483 0 0 0 0 1.0000000596046483 0 0
		 0 0 1 0 0 -2.1250001266598777 0 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4 0 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 5 ".ma";
	setAttr -s 5 ".dpf[0:4]"  4 4 4 4 4;
	setAttr -s 5 ".lw";
	setAttr -s 5 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 5;
	setAttr ".ucm" yes;
	setAttr -s 5 ".ifcl";
	setAttr -s 5 ".ifcl";
createNode dagPose -n "bindPose2";
	setAttr -s 14 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -4 0 1;
	setAttr ".wm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -2.125 0 1;
	setAttr ".wm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 2.2204460492503131e-16 0 1;
	setAttr ".wm[10]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 2.125 0 1;
	setAttr ".wm[12]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 4 0 1;
	setAttr -s 14 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 -4 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 -2.125 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[7]" -type "matrix" "xform" 0.99999994039535522 0.99999994039535522 1 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 2.2204460492503131e-16
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[9]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[10]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 2.125 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[11]" -type "matrix" "xform" 0.99999994039535522 0.99999994039535522
		 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[12]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[13]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr -s 14 ".m";
	setAttr -s 14 ".p";
	setAttr -s 14 ".g[0:13]" yes yes yes yes yes no yes no yes no yes no 
		yes no;
	setAttr ".bp" yes;
createNode groupParts -n "skinCluster1GroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[0:89]";
createNode tweak -n "tweak2";
createNode objectSet -n "tweakSet2";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId4";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts4";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode materialInfo -n "materialInfo1";
createNode shadingEngine -n "lambert2SG";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode lambert -n "swoosh_MAT";
	addAttr -ci true -sn "resolution" -ln "resolution" -dv 32 -at "long";
	setAttr ".c" -type "float3" 0 0 0 ;
	setAttr ".resolution" 256;
createNode ramp -n "ramp1";
	setAttr ".in" 4;
	setAttr -s 3 ".cel";
	setAttr ".cel[0].ep" 0.10000000149011612;
	setAttr ".cel[1].ep" 0.5;
	setAttr ".cel[2].ep" 0.89999997615814209;
createNode place2dTexture -n "place2dTexture1";
	setAttr ".mu" yes;
	setAttr ".mv" yes;
	setAttr ".wu" no;
	setAttr ".wv" no;
createNode lightLinker -s -n "lightLinker1";
	setAttr -s 3 ".lnk";
	setAttr -s 3 ".slnk";
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -s 3 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 3 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 3 ".u";
select -ne :defaultRenderingList1;
select -ne :defaultTextureList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 18 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surfaces" "Particles" "Fluids" "Image Planes" "UI:" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 18 0 1 1 1 1 1
		 1 0 0 0 0 0 0 0 0 0 0 0 ;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
connectAttr "swoosh_CTL.sy" "swoosh_CTL.sx" -l on;
connectAttr "swoosh_CTL.sy" "swoosh_CTL.sz" -l on;
connectAttr "swoosh_CTL.t" "main_all_GRP.t";
connectAttr "swoosh_CTL.r" "main_all_GRP.r";
connectAttr "swoosh_CTL.s" "main_all_GRP.s";
connectAttr "main_CTL.t" "main_control_GRP.t";
connectAttr "main_CTL.r" "main_control_GRP.r";
connectAttr "main_CTL.ro" "main_control_GRP.ro";
connectAttr "top_parent_CST.ctx" "top_control_JNT.tx";
connectAttr "top_parent_CST.cty" "top_control_JNT.ty";
connectAttr "top_parent_CST.ctz" "top_control_JNT.tz";
connectAttr "top_parent_CST.crx" "top_control_JNT.rx";
connectAttr "top_parent_CST.cry" "top_control_JNT.ry";
connectAttr "top_parent_CST.crz" "top_control_JNT.rz";
connectAttr "top_control_JNT.ro" "top_parent_CST.cro";
connectAttr "top_control_JNT.pim" "top_parent_CST.cpim";
connectAttr "top_control_JNT.rp" "top_parent_CST.crp";
connectAttr "top_control_JNT.rpt" "top_parent_CST.crt";
connectAttr "top_control_JNT.jo" "top_parent_CST.cjo";
connectAttr "top_CTL.t" "top_parent_CST.tg[1].tt";
connectAttr "top_CTL.rp" "top_parent_CST.tg[1].trp";
connectAttr "top_CTL.rpt" "top_parent_CST.tg[1].trt";
connectAttr "top_CTL.r" "top_parent_CST.tg[1].tr";
connectAttr "top_CTL.ro" "top_parent_CST.tg[1].tro";
connectAttr "top_CTL.s" "top_parent_CST.tg[1].ts";
connectAttr "top_CTL.pm" "top_parent_CST.tg[1].tpm";
connectAttr "top_parent_CST.w1" "top_parent_CST.tg[1].tw";
connectAttr "middle_parent_CST.ctx" "middle_control_JNT.tx";
connectAttr "middle_parent_CST.cty" "middle_control_JNT.ty";
connectAttr "middle_parent_CST.ctz" "middle_control_JNT.tz";
connectAttr "middle_parent_CST.crx" "middle_control_JNT.rx";
connectAttr "middle_parent_CST.cry" "middle_control_JNT.ry";
connectAttr "middle_parent_CST.crz" "middle_control_JNT.rz";
connectAttr "middle_control_JNT.ro" "middle_parent_CST.cro";
connectAttr "middle_control_JNT.pim" "middle_parent_CST.cpim";
connectAttr "middle_control_JNT.rp" "middle_parent_CST.crp";
connectAttr "middle_control_JNT.rpt" "middle_parent_CST.crt";
connectAttr "middle_control_JNT.jo" "middle_parent_CST.cjo";
connectAttr "middle_IK_CTL.t" "middle_parent_CST.tg[1].tt";
connectAttr "middle_IK_CTL.rp" "middle_parent_CST.tg[1].trp";
connectAttr "middle_IK_CTL.rpt" "middle_parent_CST.tg[1].trt";
connectAttr "middle_IK_CTL.r" "middle_parent_CST.tg[1].tr";
connectAttr "middle_IK_CTL.ro" "middle_parent_CST.tg[1].tro";
connectAttr "middle_IK_CTL.s" "middle_parent_CST.tg[1].ts";
connectAttr "middle_IK_CTL.pm" "middle_parent_CST.tg[1].tpm";
connectAttr "middle_parent_CST.w1" "middle_parent_CST.tg[1].tw";
connectAttr "bottom_parent_CST.ctx" "bottom_control_JNT.tx";
connectAttr "bottom_parent_CST.cty" "bottom_control_JNT.ty";
connectAttr "bottom_parent_CST.ctz" "bottom_control_JNT.tz";
connectAttr "bottom_parent_CST.crx" "bottom_control_JNT.rx";
connectAttr "bottom_parent_CST.cry" "bottom_control_JNT.ry";
connectAttr "bottom_parent_CST.crz" "bottom_control_JNT.rz";
connectAttr "bottom_control_JNT.ro" "bottom_parent_CST.cro";
connectAttr "bottom_control_JNT.pim" "bottom_parent_CST.cpim";
connectAttr "bottom_control_JNT.rp" "bottom_parent_CST.crp";
connectAttr "bottom_control_JNT.rpt" "bottom_parent_CST.crt";
connectAttr "bottom_control_JNT.jo" "bottom_parent_CST.cjo";
connectAttr "bottom_CTL.t" "bottom_parent_CST.tg[1].tt";
connectAttr "bottom_CTL.rp" "bottom_parent_CST.tg[1].trp";
connectAttr "bottom_CTL.rpt" "bottom_parent_CST.tg[1].trt";
connectAttr "bottom_CTL.r" "bottom_parent_CST.tg[1].tr";
connectAttr "bottom_CTL.ro" "bottom_parent_CST.tg[1].tro";
connectAttr "bottom_CTL.s" "bottom_parent_CST.tg[1].ts";
connectAttr "bottom_CTL.pm" "bottom_parent_CST.tg[1].tpm";
connectAttr "bottom_parent_CST.w1" "bottom_parent_CST.tg[1].tw";
connectAttr "spine_ribbon_SKNGroupId.id" "spline_ribbon_GEOShape.iog.og[0].gid";
connectAttr "spine_ribbon_SKNSet.mwc" "spline_ribbon_GEOShape.iog.og[0].gco";
connectAttr "groupId2.id" "spline_ribbon_GEOShape.iog.og[1].gid";
connectAttr "tweakSet1.mwc" "spline_ribbon_GEOShape.iog.og[1].gco";
connectAttr "spline_ribbon_SKN.og[0]" "spline_ribbon_GEOShape.cr";
connectAttr "tweak1.pl[0].cp[0]" "spline_ribbon_GEOShape.twl";
connectAttr "spline_01_FOLShape.ot" "spline_01_FOL.t";
connectAttr "spline_01_FOLShape.or" "spline_01_FOL.r";
connectAttr "swoosh_CTL.s" "spline_01_FOL.s";
connectAttr "spline_ribbon_GEOShape.l" "spline_01_FOLShape.is";
connectAttr "spline_ribbon_GEO.wm" "spline_01_FOLShape.iwm";
connectAttr "bottom_CTL.s" "spline_01_BND.s";
connectAttr "spline_02_FOLShape.ot" "spline_02_FOL.t";
connectAttr "spline_02_FOLShape.or" "spline_02_FOL.r";
connectAttr "swoosh_CTL.s" "spline_02_FOL.s";
connectAttr "spline_ribbon_GEOShape.l" "spline_02_FOLShape.is";
connectAttr "spline_ribbon_GEO.wm" "spline_02_FOLShape.iwm";
connectAttr "bottom_middle_sns_PMA.o3" "spline_02_BND.s";
connectAttr "spline_03_FOLShape.ot" "spline_03_FOL.t";
connectAttr "spline_03_FOLShape.or" "spline_03_FOL.r";
connectAttr "swoosh_CTL.s" "spline_03_FOL.s";
connectAttr "spline_ribbon_GEOShape.l" "spline_03_FOLShape.is";
connectAttr "spline_ribbon_GEO.wm" "spline_03_FOLShape.iwm";
connectAttr "middle_IK_CTL.s" "spline_03_BND.s";
connectAttr "spline_04_FOLShape.ot" "spline_04_FOL.t";
connectAttr "spline_04_FOLShape.or" "spline_04_FOL.r";
connectAttr "swoosh_CTL.s" "spline_04_FOL.s";
connectAttr "spline_ribbon_GEOShape.l" "spline_04_FOLShape.is";
connectAttr "spline_ribbon_GEO.wm" "spline_04_FOLShape.iwm";
connectAttr "top_middle_sns_PMA.o3" "spline_04_BND.s";
connectAttr "spline_05_FOLShape.ot" "spline_05_FOL.t";
connectAttr "spline_05_FOLShape.or" "spline_05_FOL.r";
connectAttr "swoosh_CTL.s" "spline_05_FOL.s";
connectAttr "spline_ribbon_GEOShape.l" "spline_05_FOLShape.is";
connectAttr "spline_ribbon_GEO.wm" "spline_05_FOLShape.iwm";
connectAttr "top_CTL.s" "spline_05_BND.s";
connectAttr "middle_IK_GRP_parent_CST.ctx" "middle_IK_GRP.tx";
connectAttr "middle_IK_GRP_parent_CST.cty" "middle_IK_GRP.ty";
connectAttr "middle_IK_GRP_parent_CST.ctz" "middle_IK_GRP.tz";
connectAttr "middle_IK_GRP_orient_CST.crx" "middle_IK_GRP.rx";
connectAttr "middle_IK_GRP_orient_CST.cry" "middle_IK_GRP.ry";
connectAttr "middle_IK_GRP_orient_CST.crz" "middle_IK_GRP.rz";
connectAttr "middle_IK_GRP.ro" "middle_IK_GRP_parent_CST.cro";
connectAttr "middle_IK_GRP.pim" "middle_IK_GRP_parent_CST.cpim";
connectAttr "middle_IK_GRP.rp" "middle_IK_GRP_parent_CST.crp";
connectAttr "middle_IK_GRP.rpt" "middle_IK_GRP_parent_CST.crt";
connectAttr "top_control_JNT.t" "middle_IK_GRP_parent_CST.tg[0].tt";
connectAttr "top_control_JNT.rp" "middle_IK_GRP_parent_CST.tg[0].trp";
connectAttr "top_control_JNT.rpt" "middle_IK_GRP_parent_CST.tg[0].trt";
connectAttr "top_control_JNT.r" "middle_IK_GRP_parent_CST.tg[0].tr";
connectAttr "top_control_JNT.ro" "middle_IK_GRP_parent_CST.tg[0].tro";
connectAttr "top_control_JNT.s" "middle_IK_GRP_parent_CST.tg[0].ts";
connectAttr "top_control_JNT.pm" "middle_IK_GRP_parent_CST.tg[0].tpm";
connectAttr "top_control_JNT.jo" "middle_IK_GRP_parent_CST.tg[0].tjo";
connectAttr "middle_IK_GRP_parent_CST.w0" "middle_IK_GRP_parent_CST.tg[0].tw";
connectAttr "bottom_control_JNT.t" "middle_IK_GRP_parent_CST.tg[1].tt";
connectAttr "bottom_control_JNT.rp" "middle_IK_GRP_parent_CST.tg[1].trp";
connectAttr "bottom_control_JNT.rpt" "middle_IK_GRP_parent_CST.tg[1].trt";
connectAttr "bottom_control_JNT.r" "middle_IK_GRP_parent_CST.tg[1].tr";
connectAttr "bottom_control_JNT.ro" "middle_IK_GRP_parent_CST.tg[1].tro";
connectAttr "bottom_control_JNT.s" "middle_IK_GRP_parent_CST.tg[1].ts";
connectAttr "bottom_control_JNT.pm" "middle_IK_GRP_parent_CST.tg[1].tpm";
connectAttr "bottom_control_JNT.jo" "middle_IK_GRP_parent_CST.tg[1].tjo";
connectAttr "middle_IK_GRP_parent_CST.w1" "middle_IK_GRP_parent_CST.tg[1].tw";
connectAttr "middle_IK_damper_GRP.t" "middle_IK_GRP_parent_CST.tg[2].tt";
connectAttr "middle_IK_damper_GRP.rp" "middle_IK_GRP_parent_CST.tg[2].trp";
connectAttr "middle_IK_damper_GRP.rpt" "middle_IK_GRP_parent_CST.tg[2].trt";
connectAttr "middle_IK_damper_GRP.r" "middle_IK_GRP_parent_CST.tg[2].tr";
connectAttr "middle_IK_damper_GRP.ro" "middle_IK_GRP_parent_CST.tg[2].tro";
connectAttr "middle_IK_damper_GRP.s" "middle_IK_GRP_parent_CST.tg[2].ts";
connectAttr "middle_IK_damper_GRP.pm" "middle_IK_GRP_parent_CST.tg[2].tpm";
connectAttr "middle_IK_GRP_parent_CST.w2" "middle_IK_GRP_parent_CST.tg[2].tw";
connectAttr "middle_IK_GRP.ro" "middle_IK_GRP_orient_CST.cro";
connectAttr "middle_IK_GRP.pim" "middle_IK_GRP_orient_CST.cpim";
connectAttr "top_CTL.r" "middle_IK_GRP_orient_CST.tg[0].tr";
connectAttr "top_CTL.ro" "middle_IK_GRP_orient_CST.tg[0].tro";
connectAttr "top_CTL.pm" "middle_IK_GRP_orient_CST.tg[0].tpm";
connectAttr "middle_IK_GRP_orient_CST.w0" "middle_IK_GRP_orient_CST.tg[0].tw";
connectAttr "bottom_CTL.r" "middle_IK_GRP_orient_CST.tg[1].tr";
connectAttr "bottom_CTL.ro" "middle_IK_GRP_orient_CST.tg[1].tro";
connectAttr "bottom_CTL.pm" "middle_IK_GRP_orient_CST.tg[1].tpm";
connectAttr "middle_IK_GRP_orient_CST.w1" "middle_IK_GRP_orient_CST.tg[1].tw";
connectAttr "middle_IK_damper_GRP_point_CST.ctx" "middle_IK_damper_GRP.tx";
connectAttr "middle_IK_damper_GRP_point_CST.cty" "middle_IK_damper_GRP.ty";
connectAttr "middle_IK_damper_GRP_point_CST.ctz" "middle_IK_damper_GRP.tz";
connectAttr "middle_IK_damper_GRP.pim" "middle_IK_damper_GRP_point_CST.cpim";
connectAttr "middle_IK_damper_GRP.rp" "middle_IK_damper_GRP_point_CST.crp";
connectAttr "middle_IK_damper_GRP.rpt" "middle_IK_damper_GRP_point_CST.crt";
connectAttr "top_CTL.t" "middle_IK_damper_GRP_point_CST.tg[0].tt";
connectAttr "top_CTL.rp" "middle_IK_damper_GRP_point_CST.tg[0].trp";
connectAttr "top_CTL.rpt" "middle_IK_damper_GRP_point_CST.tg[0].trt";
connectAttr "top_CTL.pm" "middle_IK_damper_GRP_point_CST.tg[0].tpm";
connectAttr "middle_IK_damper_GRP_point_CST.w0" "middle_IK_damper_GRP_point_CST.tg[0].tw"
		;
connectAttr "bottom_CTL.t" "middle_IK_damper_GRP_point_CST.tg[1].tt";
connectAttr "bottom_CTL.rp" "middle_IK_damper_GRP_point_CST.tg[1].trp";
connectAttr "bottom_CTL.rpt" "middle_IK_damper_GRP_point_CST.tg[1].trt";
connectAttr "bottom_CTL.pm" "middle_IK_damper_GRP_point_CST.tg[1].tpm";
connectAttr "middle_IK_damper_GRP_point_CST.w1" "middle_IK_damper_GRP_point_CST.tg[1].tw"
		;
connectAttr "skinCluster1GroupId.id" "swoosh_GEOShape.iog.og[0].gid";
connectAttr "skinCluster1Set.mwc" "swoosh_GEOShape.iog.og[0].gco";
connectAttr "groupId4.id" "swoosh_GEOShape.iog.og[1].gid";
connectAttr "tweakSet2.mwc" "swoosh_GEOShape.iog.og[1].gco";
connectAttr "skinCluster1.og[0]" "swoosh_GEOShape.i";
connectAttr "tweak2.vl[0].vt[0]" "swoosh_GEOShape.twl";
connectAttr "spine_ribbon_SKNGroupId.msg" "spine_ribbon_SKNSet.gn" -na;
connectAttr "spline_ribbon_GEOShape.iog.og[0]" "spine_ribbon_SKNSet.dsm" -na;
connectAttr "spline_ribbon_SKN.msg" "spine_ribbon_SKNSet.ub[0]";
connectAttr "spine_ribbon_SKNGroupParts.og" "spline_ribbon_SKN.ip[0].ig";
connectAttr "spine_ribbon_SKNGroupId.id" "spline_ribbon_SKN.ip[0].gi";
connectAttr "bindPose1.msg" "spline_ribbon_SKN.bp";
connectAttr "bottom_control_JNT.wm" "spline_ribbon_SKN.ma[0]";
connectAttr "middle_control_JNT.wm" "spline_ribbon_SKN.ma[1]";
connectAttr "top_control_JNT.wm" "spline_ribbon_SKN.ma[2]";
connectAttr "bottom_control_JNT.liw" "spline_ribbon_SKN.lw[0]";
connectAttr "middle_control_JNT.liw" "spline_ribbon_SKN.lw[1]";
connectAttr "top_control_JNT.liw" "spline_ribbon_SKN.lw[2]";
connectAttr "bottom_control_JNT.obcc" "spline_ribbon_SKN.ifcl[0]";
connectAttr "middle_control_JNT.obcc" "spline_ribbon_SKN.ifcl[1]";
connectAttr "top_control_JNT.obcc" "spline_ribbon_SKN.ifcl[2]";
connectAttr "bottom_control_JNT.msg" "bindPose1.m[0]";
connectAttr "middle_control_JNT.msg" "bindPose1.m[1]";
connectAttr "top_control_JNT.msg" "bindPose1.m[2]";
connectAttr "bindPose1.w" "bindPose1.p[0]";
connectAttr "bindPose1.w" "bindPose1.p[1]";
connectAttr "bindPose1.w" "bindPose1.p[2]";
connectAttr "bottom_control_JNT.bps" "bindPose1.wm[0]";
connectAttr "middle_control_JNT.bps" "bindPose1.wm[1]";
connectAttr "top_control_JNT.bps" "bindPose1.wm[2]";
connectAttr "tweak1.og[0]" "spine_ribbon_SKNGroupParts.ig";
connectAttr "spine_ribbon_SKNGroupId.id" "spine_ribbon_SKNGroupParts.gi";
connectAttr "groupParts2.og" "tweak1.ip[0].ig";
connectAttr "groupId2.id" "tweak1.ip[0].gi";
connectAttr "groupId2.msg" "tweakSet1.gn" -na;
connectAttr "spline_ribbon_GEOShape.iog.og[1]" "tweakSet1.dsm" -na;
connectAttr "tweak1.msg" "tweakSet1.ub[0]";
connectAttr "spline_ribbon_GEOShapeOrig.ws" "groupParts2.ig";
connectAttr "groupId2.id" "groupParts2.gi";
connectAttr "bottom_CTL.s" "bottom_middle_sns_PMA.i3[0]";
connectAttr "middle_IK_CTL.s" "bottom_middle_sns_PMA.i3[1]";
connectAttr "top_CTL.s" "top_middle_sns_PMA.i3[0]";
connectAttr "middle_IK_CTL.s" "top_middle_sns_PMA.i3[1]";
connectAttr "skinCluster1GroupId.msg" "skinCluster1Set.gn" -na;
connectAttr "swoosh_GEOShape.iog.og[0]" "skinCluster1Set.dsm" -na;
connectAttr "skinCluster1.msg" "skinCluster1Set.ub[0]";
connectAttr "skinCluster1GroupParts.og" "skinCluster1.ip[0].ig";
connectAttr "skinCluster1GroupId.id" "skinCluster1.ip[0].gi";
connectAttr "bindPose2.msg" "skinCluster1.bp";
connectAttr "spline_01_BND.wm" "skinCluster1.ma[0]";
connectAttr "spline_02_BND.wm" "skinCluster1.ma[1]";
connectAttr "spline_03_BND.wm" "skinCluster1.ma[2]";
connectAttr "spline_04_BND.wm" "skinCluster1.ma[3]";
connectAttr "spline_05_BND.wm" "skinCluster1.ma[4]";
connectAttr "spline_01_BND.liw" "skinCluster1.lw[0]";
connectAttr "spline_02_BND.liw" "skinCluster1.lw[1]";
connectAttr "spline_03_BND.liw" "skinCluster1.lw[2]";
connectAttr "spline_04_BND.liw" "skinCluster1.lw[3]";
connectAttr "spline_05_BND.liw" "skinCluster1.lw[4]";
connectAttr "spline_01_BND.obcc" "skinCluster1.ifcl[0]";
connectAttr "spline_02_BND.obcc" "skinCluster1.ifcl[1]";
connectAttr "spline_03_BND.obcc" "skinCluster1.ifcl[2]";
connectAttr "spline_04_BND.obcc" "skinCluster1.ifcl[3]";
connectAttr "spline_05_BND.obcc" "skinCluster1.ifcl[4]";
connectAttr "spline_01_BND.msg" "skinCluster1.ptt";
connectAttr "rig_all_GRP.msg" "bindPose2.m[0]";
connectAttr "main_all_GRP.msg" "bindPose2.m[1]";
connectAttr "main_control_GRP.msg" "bindPose2.m[2]";
connectAttr "spline_bind_joint_GRP.msg" "bindPose2.m[3]";
connectAttr "spline_01_FOL.msg" "bindPose2.m[4]";
connectAttr "spline_01_BND.msg" "bindPose2.m[5]";
connectAttr "spline_02_FOL.msg" "bindPose2.m[6]";
connectAttr "spline_02_BND.msg" "bindPose2.m[7]";
connectAttr "spline_03_FOL.msg" "bindPose2.m[8]";
connectAttr "spline_03_BND.msg" "bindPose2.m[9]";
connectAttr "spline_04_FOL.msg" "bindPose2.m[10]";
connectAttr "spline_04_BND.msg" "bindPose2.m[11]";
connectAttr "spline_05_FOL.msg" "bindPose2.m[12]";
connectAttr "spline_05_BND.msg" "bindPose2.m[13]";
connectAttr "bindPose2.w" "bindPose2.p[0]";
connectAttr "bindPose2.m[0]" "bindPose2.p[1]";
connectAttr "bindPose2.m[1]" "bindPose2.p[2]";
connectAttr "bindPose2.m[2]" "bindPose2.p[3]";
connectAttr "bindPose2.m[3]" "bindPose2.p[4]";
connectAttr "bindPose2.m[4]" "bindPose2.p[5]";
connectAttr "bindPose2.m[3]" "bindPose2.p[6]";
connectAttr "bindPose2.m[6]" "bindPose2.p[7]";
connectAttr "bindPose2.m[3]" "bindPose2.p[8]";
connectAttr "bindPose2.m[8]" "bindPose2.p[9]";
connectAttr "bindPose2.m[3]" "bindPose2.p[10]";
connectAttr "bindPose2.m[10]" "bindPose2.p[11]";
connectAttr "bindPose2.m[3]" "bindPose2.p[12]";
connectAttr "bindPose2.m[12]" "bindPose2.p[13]";
connectAttr "spline_01_BND.bps" "bindPose2.wm[5]";
connectAttr "spline_02_BND.bps" "bindPose2.wm[7]";
connectAttr "spline_03_BND.bps" "bindPose2.wm[9]";
connectAttr "spline_04_BND.bps" "bindPose2.wm[11]";
connectAttr "spline_05_BND.bps" "bindPose2.wm[13]";
connectAttr "tweak2.og[0]" "skinCluster1GroupParts.ig";
connectAttr "skinCluster1GroupId.id" "skinCluster1GroupParts.gi";
connectAttr "groupParts4.og" "tweak2.ip[0].ig";
connectAttr "groupId4.id" "tweak2.ip[0].gi";
connectAttr "groupId4.msg" "tweakSet2.gn" -na;
connectAttr "swoosh_GEOShape.iog.og[1]" "tweakSet2.dsm" -na;
connectAttr "tweak2.msg" "tweakSet2.ub[0]";
connectAttr "swoosh_GEOShape1Orig.w" "groupParts4.ig";
connectAttr "groupId4.id" "groupParts4.gi";
connectAttr "lambert2SG.msg" "materialInfo1.sg";
connectAttr "swoosh_MAT.msg" "materialInfo1.m";
connectAttr "swoosh_MAT.msg" "materialInfo1.t" -na;
connectAttr "swoosh_MAT.oc" "lambert2SG.ss";
connectAttr "swoosh_GEOShape.iog" "lambert2SG.dsm" -na;
connectAttr "ramp1.oc" "swoosh_MAT.it";
connectAttr "place2dTexture1.o" "ramp1.uv";
connectAttr "place2dTexture1.ofs" "ramp1.fs";
connectAttr "bottom_CTL.transparency" "ramp1.cel[0].ecr";
connectAttr "bottom_CTL.transparency" "ramp1.cel[0].ecg";
connectAttr "bottom_CTL.transparency" "ramp1.cel[0].ecb";
connectAttr "middle_IK_CTL.transparency" "ramp1.cel[1].ecr";
connectAttr "middle_IK_CTL.transparency" "ramp1.cel[1].ecg";
connectAttr "middle_IK_CTL.transparency" "ramp1.cel[1].ecb";
connectAttr "top_CTL.transparency" "ramp1.cel[2].ecr";
connectAttr "top_CTL.transparency" "ramp1.cel[2].ecg";
connectAttr "top_CTL.transparency" "ramp1.cel[2].ecb";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert2SG.message" ":defaultLightSet.message";
connectAttr "lambert2SG.pa" ":renderPartition.st" -na;
connectAttr "swoosh_MAT.msg" ":defaultShaderList1.s" -na;
connectAttr "top_middle_sns_PMA.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "bottom_middle_sns_PMA.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "place2dTexture1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "ramp1.msg" ":defaultTextureList1.tx" -na;
// End of Swoosh.ma
