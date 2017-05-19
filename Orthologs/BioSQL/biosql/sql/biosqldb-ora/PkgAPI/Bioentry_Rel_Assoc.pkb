--
-- API Package Body for Bioentry_Rel_Assoc.
--
-- Scaffold auto-generated by gen-api.pl (H.Lapp, 2002).
--
-- $Id: Bioentry_Rel_Assoc.pkb,v 1.1.1.1 2002-08-13 19:51:10 lapp Exp $
--

--
-- Copyright 2002-2003 Genomics Institute of the Novartis Research Foundation
-- Copyright 2002-2008 Hilmar Lapp
-- 
--  This file is part of BioSQL.
--
--  BioSQL is free software: you can redistribute it and/or modify it
--  under the terms of the GNU Lesser General Public License as
--  published by the Free Software Foundation, either version 3 of the
--  License, or (at your option) any later version.
--
--  BioSQL is distributed in the hope that it will be useful,
--  but WITHOUT ANY WARRANTY; without even the implied warranty of
--  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
--  GNU Lesser General Public License for more details.
--
--  You should have received a copy of the GNU Lesser General Public License
--  along with BioSQL. If not, see <http://www.gnu.org/licenses/>.
--

CREATE OR REPLACE
PACKAGE BODY EntRelA IS

CURSOR EntRelA_c (
		EntRelA_REL_OID	IN SG_BIOENTRY_REL_ASSOC.REL_OID%TYPE,
		EntRelA_ENT_OID	IN SG_BIOENTRY_REL_ASSOC.ENT_OID%TYPE)
RETURN SG_BIOENTRY_REL_ASSOC%ROWTYPE IS
	SELECT t.* FROM SG_BIOENTRY_REL_ASSOC t
	WHERE
		t.Rel_Oid = EntRelA_Rel_Oid
	AND     t.Ent_Oid = EntRelA_Ent_Oid
	;

FUNCTION get_oid(
		REL_OID	IN SG_BIOENTRY_REL_ASSOC.REL_OID%TYPE DEFAULT NULL,
		ENT_OID	IN SG_BIOENTRY_REL_ASSOC.ENT_OID%TYPE DEFAULT NULL,
		Ent_ACCESSION	IN SG_BIOENTRY.ACCESSION%TYPE DEFAULT NULL,
		Ent_VERSION	IN SG_BIOENTRY.VERSION%TYPE DEFAULT NULL,
		Ent_IDENTIFIER	IN SG_BIOENTRY.IDENTIFIER%TYPE DEFAULT NULL,
		DB_OID		IN SG_BIOENTRY.DB_OID%TYPE DEFAULT NULL,
		DB_NAME		IN SG_BIODATABASE.NAME%TYPE DEFAULT NULL,
		DB_ACRONYM	IN SG_BIODATABASE.ACRONYM%TYPE DEFAULT NULL,
		Rel_VERSION	IN SG_DB_RELEASE.VERSION%TYPE DEFAULT NULL,
		Rel_Rel_DATE	IN SG_DB_RELEASE.REL_DATE%TYPE DEFAULT NULL,
		do_DML		IN NUMBER DEFAULT BSStd.DML_NO)
RETURN INTEGER
IS
	pk	INTEGER DEFAULT NULL;
	EntRelA_row EntRelA_c%ROWTYPE;
	ENT_OID_	SG_BIOENTRY.OID%TYPE DEFAULT ENT_OID;
	REL_OID_	SG_DB_RELEASE.OID%TYPE DEFAULT REL_OID;
BEGIN
	-- look up SG_BIOENTRY
	IF (ENT_OID_ IS NULL) THEN
		ENT_OID_ := Ent.get_oid(
				Ent_ACCESSION => Ent_ACCESSION,
				Ent_VERSION => Ent_VERSION,
				Ent_IDENTIFIER => Ent_IDENTIFIER,
				DB_OID => DB_OID,
				DB_Name => DB_Name,
				DB_Acronym => DB_Acronym);
	END IF;
	-- look up SG_DB_RELEASE
	IF (REL_OID_ IS NULL) THEN
		REL_OID_ := Rel.get_oid(
				Rel_VERSION => Rel_VERSION,
				Rel_Rel_DATE => Rel_Rel_DATE,
				DB_OID => DB_OID,
				DB_Name => DB_Name,
				DB_Acronym => DB_Acronym,
				do_DML => do_DML);
	END IF;
	-- look up
	FOR EntRelA_row IN EntRelA_c (Rel_Oid_, Ent_Oid_) LOOP
	        pk := 1;
	END LOOP;
	-- insert if requested (no update)
	IF (pk IS NULL) AND 
	   ((do_DML = BSStd.DML_I) OR (do_DML = BSStd.DML_UI)) THEN
	    	-- look up foreign keys if not provided:
		-- look up SG_BIOENTRY successful?
		IF (ENT_OID_ IS NULL) THEN
			raise_application_error(-20101,
				'failed to look up Ent <' || Ent_ACCESSION || '|' || Ent_VERSION || '|' || DB_OID || '|' || Ent_IDENTIFIER || '>');
		END IF;
		-- look up SG_DB_RELEASE successful?
		IF (REL_OID_ IS NULL) THEN
			raise_application_error(-20101,
				'failed to look up Rel <' || Rel_VERSION || '|' || DB_OID || '>');
		END IF;
	    	-- insert the record and obtain the primary key
	    	pk := do_insert(
			REL_OID => REL_OID_,
		        ENT_OID => ENT_OID_);
	END IF;
	-- return the primary key
	RETURN pk;
END;

FUNCTION do_insert(
		REL_OID	IN SG_BIOENTRY_REL_ASSOC.REL_OID%TYPE,
		ENT_OID	IN SG_BIOENTRY_REL_ASSOC.ENT_OID%TYPE)
RETURN INTEGER
IS
BEGIN
	-- insert the record
	INSERT INTO SG_BIOENTRY_REL_ASSOC (
		REL_OID,
		ENT_OID)
	VALUES (REL_OID,
		ENT_OID)
	;
	-- return true
	RETURN 1;
END;

END EntRelA;
/

