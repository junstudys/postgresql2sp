CREATE OR REPLACE FUNCTION {sp_nm}(i_start_dt character varying, i_end_dt character varying)
  RETURNS integer AS
$BODY$
 /* *******************************************************
*功能名称--NAME         :{sp_nm}(i_start_dt character varying, i_end_dt character varying)
*功能描述--COMMENT      :{sp_nm_rmk}
*功能层次--LEVEL        :
*执行周期--PERIOD       :
*参数    --PARAM        :i_start_dt:开始日期:格式如'yyyymmdd hh:mi:ss'
*参数    --PARAM        :i_end_dt  :结束日期:格式如'yyyymmdd hh:mi:ss'
*参数    --PARAM        :i_end_dt  :结束日期:格式如'yyyymmdd hh:mi:ss'
*参数    --PARAM        :成功返加0;错误返回1
*备注    --REMARK       :调用方式：select {sp_nm}('20240101 00:00:00','20240131 23:59:59');
*创建作者--CREATOR      :
*创建时间--CREATED_TIME :{created_time}

*修改作者--MODIFIED BY  :
*修改时间--MODIFIED_TIME:
*修改记录--MODIFY       :

*来源表  --FROM         :
*来源表  --FROM         :
*来源表  --FROM         :
*目标表  --TO           :
**********************************************************/

 --日志操作记录行
DECLARE
int_return               INTEGER;
START_TM                 TIMESTAMP(0) without TIME ZONE;
END_TM                   TIMESTAMP(0) without TIME ZONE;
START_TM_PRE             TIMESTAMP(0) without TIME ZONE;
END_TM_NXT               TIMESTAMP(0) without TIME ZONE;
START_DT                 date;
END_DT                   date;
START_DT_NXT10           date;
END_DT_NXT10             date;
START_DT_NXT10_PRE       date;
END_DT_NXT10_NXT         date;
START_DT_PRE             date;
END_DT_NXT               date;
START_TM_HR              VARCHAR;
END_TM_HR                VARCHAR;
START_TM_PRE_HR          VARCHAR;
END_TM_NXT_HR            VARCHAR;
vc_sql                   text;
v_start_time             TIMESTAMP(0) without TIME ZONE;--执行开始时间
v_end_time               TIMESTAMP(0) without TIME ZONE;--执行结束时间

BEGIN
START_TM            := i_start_dt::TIMESTAMP;
END_TM              := i_end_dt::TIMESTAMP;
START_TM_PRE        := START_TM - interval '15 day'; --向前偏移15天
END_TM_NXT          := END_TM + interval '20 day';
START_DT            := i_start_dt::date;
END_DT              := i_end_dt::date;
START_DT_NXT10      := START_DT + interval '10 day';  --开始日期后移10天
END_DT_NXT10        := END_DT + interval '10 day';    --结束日期后移10天
START_DT_NXT10_PRE  := START_DT_NXT10 - interval '15 day';
END_DT_NXT10_NXT    := END_DT_NXT10 + interval '20 day';
START_DT_PRE        := (START_TM - interval '15 day')::date; --向前偏移15天
END_DT_NXT          := (END_TM + interval '20 day')::date;
START_TM_HR         :=to_char(START_TM,'yyyymmdd')||'00';
END_TM_HR           :=to_char(END_TM,'yyyymmdd')||'23';
START_TM_PRE_HR     :=to_char(START_TM_PRE,'yyyymmdd')||'00';
END_TM_NXT_HR       :=to_char(END_TM_NXT,'yyyymmdd')||'23';


{sp_body_text}

--输出整个存储过程执行时间
RAISE notice '%, %{sp_nm} execute ok', TIMEOFDAY() ::TIMESTAMP - NOW(), TIMEOFDAY() ::TIMESTAMP;
return 0;
END;
$BODY$
LANGUAGE plpgsql VOLATILE;
COMMENT ON FUNCTION {sp_nm}(i_start_dt character varying, i_end_dt character varying) IS '{sp_nm_rmk}';
