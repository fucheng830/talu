INSERT INTO public.agent (id,"name",description,system_prompt,opening_question,knowledge,tools,voice,avatar,suggestion,user_id,"permission",category,llm,gid,opening_text,isplus) VALUES
	 ('aa233431-5c2b-4875-90bc-ac82f9ae5a0f','GPT-3.5','GPT-3.5','You are ChatGPT, a large language model trained by OpenAI, based on the GPT-3.5 architecture.','[]','[]','[]',NULL,'https://cos.aitutu.cc/gpts/3.5net.png','{"is_enable": true, "custom_prompt": ""}','5c732eba-4320-485c-a440-a4e0cda614a4','public','Recommended','{
  "model": "v1",
  "temperature": 0.8,
  "streaming": true
}','','',true),
	 ('4287b7c8-dacd-49e1-aed9-db097acc1860','GPT-4.0','GPT-4.0','You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture.
Knowledge cutoff: 2023-04
Current date: 2023-11-10','[]','[]','[]',NULL,'https://cos.aitutu.cc/gpts/gpt4all.jpg','{"is_enable": true, "custom_prompt": ""}','5c732eba-4320-485c-a440-a4e0cda614a4','public','Recommended','{
  "model": "v2",
  "temperature": 0.8,
  "streaming": true
}','','',true);

INSERT INTO public.agent_category (id,"name",description) VALUES
	 ('5c154a20-3893-4a71-951e-916499cdecd8','Recommended',NULL);

INSERT INTO public.users (user_id,union_id,openid,"name",avatar,subscribe_scene,"password",phone_num,session_key,vip_end_time,status,register_time,user_info,email,referee,ip) VALUES
	 ('5c732eba-4320-485c-a440-a4e0cda614a4','admin_union_id','admin_openid','Admin User','/avatar.jpg','Admin Scene','e10adc3949ba59abbe56e057f20f883e','1234567890','admin_session_key','2050-05-08 03:12:49.566',9,'2024-05-08 03:12:49.566128','{"usable_token": 30}','admin@example.com','2e631d38-2aec-4ab3-bc5f-29ff304d0be2','127.0.0.1');

