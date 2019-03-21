-- JD_db***********************************************************************************************
use day8;
create table jd_data(
	id int auto_increment primary key, 
	img varchar(580),
	price varchar(580),
	shop_desc varchar(580),
	commentNum varchar(580),
	store varchar(580),
	sku  varchar(580),
	href varchar(580),
	store_link varchar(580),
	create_time timestamp not null default current_timestamp
        );