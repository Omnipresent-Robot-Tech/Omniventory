PGDMP     %                    y            omni-inventory    13.2    13.2 U    -           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            .           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            /           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            0           1262    49730    omni-inventory    DATABASE     t   CREATE DATABASE "omni-inventory" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';
     DROP DATABASE "omni-inventory";
                postgres    false            ?           1247    49732    roles    TYPE     E   CREATE TYPE public.roles AS ENUM (
    'superadmin',
    'client'
);
    DROP TYPE public.roles;
       public          postgres    false            ?            1259    74544    images    TABLE     ?   CREATE TABLE public.images (
    id bigint NOT NULL,
    image_of character varying(100) NOT NULL,
    filename character varying(250) DEFAULT 'undefined'::character varying NOT NULL,
    image text NOT NULL,
    external_id bigint NOT NULL
);
    DROP TABLE public.images;
       public         heap    postgres    false            ?            1259    74542    images_id_seq    SEQUENCE     v   CREATE SEQUENCE public.images_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.images_id_seq;
       public          postgres    false    217            1           0    0    images_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.images_id_seq OWNED BY public.images.id;
          public          postgres    false    216            ?            1259    58018 	   inventory    TABLE     ?   CREATE TABLE public.inventory (
    id bigint NOT NULL,
    product_id bigint NOT NULL,
    status smallint DEFAULT 1 NOT NULL,
    created_on timestamp without time zone DEFAULT now() NOT NULL
);
    DROP TABLE public.inventory;
       public         heap    postgres    false            2           0    0    COLUMN inventory.status    COMMENT     c   COMMENT ON COLUMN public.inventory.status IS '1: Available
2: In-use
0: Broken/Under-maintenance';
          public          postgres    false    209            ?            1259    58016    inventory_id_seq    SEQUENCE     y   CREATE SEQUENCE public.inventory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.inventory_id_seq;
       public          postgres    false    209            3           0    0    inventory_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.inventory_id_seq OWNED BY public.inventory.id;
          public          postgres    false    208            ?            1259    58032    item_issued    TABLE     %  CREATE TABLE public.item_issued (
    id bigint NOT NULL,
    item_id bigint NOT NULL,
    issued_on timestamp without time zone DEFAULT now() NOT NULL,
    issued_to bigint NOT NULL,
    expected_return timestamp without time zone NOT NULL,
    remarks text,
    returned boolean DEFAULT false NOT NULL,
    approved_by bigint NOT NULL,
    received_by bigint,
    location character varying(150) DEFAULT 'Omni Headquarters'::character varying NOT NULL,
    returned_on timestamp without time zone,
    transfered boolean DEFAULT false NOT NULL
);
    DROP TABLE public.item_issued;
       public         heap    postgres    false            ?            1259    58030    item_assignment_id_seq    SEQUENCE        CREATE SEQUENCE public.item_assignment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.item_assignment_id_seq;
       public          postgres    false    211            4           0    0    item_assignment_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.item_assignment_id_seq OWNED BY public.item_issued.id;
          public          postgres    false    210            ?            1259    66320    maintenance_log    TABLE     @  CREATE TABLE public.maintenance_log (
    id bigint NOT NULL,
    item_id bigint NOT NULL,
    broken_on timestamp without time zone,
    created_on timestamp without time zone NOT NULL,
    short_description text NOT NULL,
    status character varying(100) NOT NULL,
    status_updated_on timestamp without time zone NOT NULL,
    created_by bigint NOT NULL,
    repaired boolean DEFAULT false NOT NULL,
    status_updated_by bigint NOT NULL,
    closed_by bigint,
    closed_on timestamp without time zone,
    description text,
    title character varying(250) NOT NULL
);
 #   DROP TABLE public.maintenance_log;
       public         heap    postgres    false            ?            1259    66318    maintenance_log_id_seq    SEQUENCE        CREATE SEQUENCE public.maintenance_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.maintenance_log_id_seq;
       public          postgres    false    215            5           0    0    maintenance_log_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.maintenance_log_id_seq OWNED BY public.maintenance_log.id;
          public          postgres    false    214            ?            1259    66277    order    TABLE     ?  CREATE TABLE public."order" (
    id bigint NOT NULL,
    product_ids_qty json[] NOT NULL,
    created_on timestamp without time zone DEFAULT now() NOT NULL,
    ordered_by bigint NOT NULL,
    approved_by bigint,
    approved_on timestamp without time zone,
    remarks text,
    location character varying(150),
    approved boolean DEFAULT false NOT NULL,
    expected_return timestamp without time zone NOT NULL,
    status character varying(50) NOT NULL
);
    DROP TABLE public."order";
       public         heap    postgres    false            ?            1259    66275    order_id_seq    SEQUENCE     u   CREATE SEQUENCE public.order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.order_id_seq;
       public          postgres    false    213            6           0    0    order_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.order_id_seq OWNED BY public."order".id;
          public          postgres    false    212            ?            1259    57936    product    TABLE     ?  CREATE TABLE public.product (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    category integer NOT NULL,
    vendor_name character varying(100),
    vendor_phone character varying(15),
    vendor_email character varying(150),
    description text,
    short_description text NOT NULL,
    posted_by bigint NOT NULL,
    created_on time without time zone DEFAULT now() NOT NULL,
    critical_limit integer DEFAULT 1 NOT NULL
);
    DROP TABLE public.product;
       public         heap    postgres    false            ?            1259    57924    product_category    TABLE     p   CREATE TABLE public.product_category (
    id integer NOT NULL,
    category character varying(150) NOT NULL
);
 $   DROP TABLE public.product_category;
       public         heap    postgres    false            ?            1259    57934    product_id_seq    SEQUENCE     ?   CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.product_id_seq;
       public          postgres    false    205            7           0    0    product_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;
          public          postgres    false    204            ?            1259    57958    product_images    TABLE     ?   CREATE TABLE public.product_images (
    id bigint NOT NULL,
    show boolean DEFAULT true NOT NULL,
    filename character varying(250) NOT NULL,
    product_id bigint NOT NULL,
    image text NOT NULL
);
 "   DROP TABLE public.product_images;
       public         heap    postgres    false            ?            1259    57956    product_images_id_seq    SEQUENCE     ~   CREATE SEQUENCE public.product_images_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.product_images_id_seq;
       public          postgres    false    207            8           0    0    product_images_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.product_images_id_seq OWNED BY public.product_images.id;
          public          postgres    false    206            ?            1259    57922    product_type_id_seq    SEQUENCE     ?   CREATE SEQUENCE public.product_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.product_type_id_seq;
       public          postgres    false    203            9           0    0    product_type_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.product_type_id_seq OWNED BY public.product_category.id;
          public          postgres    false    202            ?            1259    49739    users    TABLE     6  CREATE TABLE public.users (
    id bigint NOT NULL,
    fname character varying(50) NOT NULL,
    lname character varying(50),
    role public.roles NOT NULL,
    verified boolean DEFAULT false NOT NULL,
    email character varying(150) NOT NULL,
    password text NOT NULL,
    phone character varying(11)
);
    DROP TABLE public.users;
       public         heap    postgres    false    640            ?            1259    49737    users_id_seq    SEQUENCE     u   CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    201            :           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    200            q           2604    74547 	   images id    DEFAULT     f   ALTER TABLE ONLY public.images ALTER COLUMN id SET DEFAULT nextval('public.images_id_seq'::regclass);
 8   ALTER TABLE public.images ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    217    217            d           2604    58021    inventory id    DEFAULT     l   ALTER TABLE ONLY public.inventory ALTER COLUMN id SET DEFAULT nextval('public.inventory_id_seq'::regclass);
 ;   ALTER TABLE public.inventory ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    209    208    209            g           2604    58035    item_issued id    DEFAULT     t   ALTER TABLE ONLY public.item_issued ALTER COLUMN id SET DEFAULT nextval('public.item_assignment_id_seq'::regclass);
 =   ALTER TABLE public.item_issued ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    210    211    211            o           2604    66323    maintenance_log id    DEFAULT     x   ALTER TABLE ONLY public.maintenance_log ALTER COLUMN id SET DEFAULT nextval('public.maintenance_log_id_seq'::regclass);
 A   ALTER TABLE public.maintenance_log ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    214    215    215            l           2604    66280    order id    DEFAULT     f   ALTER TABLE ONLY public."order" ALTER COLUMN id SET DEFAULT nextval('public.order_id_seq'::regclass);
 9   ALTER TABLE public."order" ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    212    213    213            _           2604    57939 
   product id    DEFAULT     h   ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);
 9   ALTER TABLE public.product ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    205    204    205            ^           2604    57927    product_category id    DEFAULT     v   ALTER TABLE ONLY public.product_category ALTER COLUMN id SET DEFAULT nextval('public.product_type_id_seq'::regclass);
 B   ALTER TABLE public.product_category ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    203    202    203            b           2604    57961    product_images id    DEFAULT     v   ALTER TABLE ONLY public.product_images ALTER COLUMN id SET DEFAULT nextval('public.product_images_id_seq'::regclass);
 @   ALTER TABLE public.product_images ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    207    206    207            \           2604    49742    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    201    200    201            *          0    74544    images 
   TABLE DATA           L   COPY public.images (id, image_of, filename, image, external_id) FROM stdin;
    public          postgres    false    217   ?g       "          0    58018 	   inventory 
   TABLE DATA           G   COPY public.inventory (id, product_id, status, created_on) FROM stdin;
    public          postgres    false    209   ph       $          0    58032    item_issued 
   TABLE DATA           ?   COPY public.item_issued (id, item_id, issued_on, issued_to, expected_return, remarks, returned, approved_by, received_by, location, returned_on, transfered) FROM stdin;
    public          postgres    false    211   /i       (          0    66320    maintenance_log 
   TABLE DATA           ?   COPY public.maintenance_log (id, item_id, broken_on, created_on, short_description, status, status_updated_on, created_by, repaired, status_updated_by, closed_by, closed_on, description, title) FROM stdin;
    public          postgres    false    215   9l       &          0    66277    order 
   TABLE DATA           ?   COPY public."order" (id, product_ids_qty, created_on, ordered_by, approved_by, approved_on, remarks, location, approved, expected_return, status) FROM stdin;
    public          postgres    false    213   ?m                 0    57936    product 
   TABLE DATA           ?   COPY public.product (id, name, category, vendor_name, vendor_phone, vendor_email, description, short_description, posted_by, created_on, critical_limit) FROM stdin;
    public          postgres    false    205   ?m                 0    57924    product_category 
   TABLE DATA           8   COPY public.product_category (id, category) FROM stdin;
    public          postgres    false    203   p                  0    57958    product_images 
   TABLE DATA           O   COPY public.product_images (id, show, filename, product_id, image) FROM stdin;
    public          postgres    false    207   tp                 0    49739    users 
   TABLE DATA           Y   COPY public.users (id, fname, lname, role, verified, email, password, phone) FROM stdin;
    public          postgres    false    201   (q       ;           0    0    images_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.images_id_seq', 1, true);
          public          postgres    false    216            <           0    0    inventory_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.inventory_id_seq', 37, true);
          public          postgres    false    208            =           0    0    item_assignment_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.item_assignment_id_seq', 35, true);
          public          postgres    false    210            >           0    0    maintenance_log_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.maintenance_log_id_seq', 4, true);
          public          postgres    false    214            ?           0    0    order_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.order_id_seq', 1, false);
          public          postgres    false    212            @           0    0    product_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.product_id_seq', 8, true);
          public          postgres    false    204            A           0    0    product_images_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.product_images_id_seq', 3, true);
          public          postgres    false    206            B           0    0    product_type_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.product_type_id_seq', 8, true);
          public          postgres    false    202            C           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 5, true);
          public          postgres    false    200            x           2606    57929    product_category id_pk 
   CONSTRAINT     T   ALTER TABLE ONLY public.product_category
    ADD CONSTRAINT id_pk PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.product_category DROP CONSTRAINT id_pk;
       public            postgres    false    203            ?           2606    74553    images images_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.images DROP CONSTRAINT images_pkey;
       public            postgres    false    217            ?           2606    58024    inventory inventory_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.inventory DROP CONSTRAINT inventory_pkey;
       public            postgres    false    209            ?           2606    58042     item_issued item_assignment_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.item_issued
    ADD CONSTRAINT item_assignment_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.item_issued DROP CONSTRAINT item_assignment_pkey;
       public            postgres    false    211            ?           2606    66329 $   maintenance_log maintenance_log_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.maintenance_log
    ADD CONSTRAINT maintenance_log_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.maintenance_log DROP CONSTRAINT maintenance_log_pkey;
       public            postgres    false    215            ?           2606    66287    order pk_id 
   CONSTRAINT     K   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT pk_id PRIMARY KEY (id);
 7   ALTER TABLE ONLY public."order" DROP CONSTRAINT pk_id;
       public            postgres    false    213            ~           2606    57966 "   product_images product_images_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.product_images
    ADD CONSTRAINT product_images_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.product_images DROP CONSTRAINT product_images_pkey;
       public            postgres    false    207            |           2606    57944    product product_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.product DROP CONSTRAINT product_pkey;
       public            postgres    false    205            z           2606    57933     product_category unique_category 
   CONSTRAINT     _   ALTER TABLE ONLY public.product_category
    ADD CONSTRAINT unique_category UNIQUE (category);
 J   ALTER TABLE ONLY public.product_category DROP CONSTRAINT unique_category;
       public            postgres    false    203            t           2606    49750    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public            postgres    false    201            v           2606    49748    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    201            ?           2606    66293    order approved_by_fk    FK CONSTRAINT     y   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT approved_by_fk FOREIGN KEY (approved_by) REFERENCES public.users(id);
 @   ALTER TABLE ONLY public."order" DROP CONSTRAINT approved_by_fk;
       public          postgres    false    213    2934    201            ?           2606    58053    item_issued aproved_by_fk    FK CONSTRAINT     |   ALTER TABLE ONLY public.item_issued
    ADD CONSTRAINT aproved_by_fk FOREIGN KEY (approved_by) REFERENCES public.users(id);
 C   ALTER TABLE ONLY public.item_issued DROP CONSTRAINT aproved_by_fk;
       public          postgres    false    2934    211    201            ?           2606    57945    product category_pk    FK CONSTRAINT     ~   ALTER TABLE ONLY public.product
    ADD CONSTRAINT category_pk FOREIGN KEY (category) REFERENCES public.product_category(id);
 =   ALTER TABLE ONLY public.product DROP CONSTRAINT category_pk;
       public          postgres    false    203    2936    205            ?           2606    66345    maintenance_log closed_by_fk    FK CONSTRAINT     }   ALTER TABLE ONLY public.maintenance_log
    ADD CONSTRAINT closed_by_fk FOREIGN KEY (closed_by) REFERENCES public.users(id);
 F   ALTER TABLE ONLY public.maintenance_log DROP CONSTRAINT closed_by_fk;
       public          postgres    false    201    215    2934            ?           2606    66330    maintenance_log created_by_fk    FK CONSTRAINT        ALTER TABLE ONLY public.maintenance_log
    ADD CONSTRAINT created_by_fk FOREIGN KEY (created_by) REFERENCES public.users(id);
 G   ALTER TABLE ONLY public.maintenance_log DROP CONSTRAINT created_by_fk;
       public          postgres    false    2934    201    215            ?           2606    58048    item_issued issued_to_fk    FK CONSTRAINT     y   ALTER TABLE ONLY public.item_issued
    ADD CONSTRAINT issued_to_fk FOREIGN KEY (issued_to) REFERENCES public.users(id);
 B   ALTER TABLE ONLY public.item_issued DROP CONSTRAINT issued_to_fk;
       public          postgres    false    2934    211    201            ?           2606    58043    item_issued item_id_fk    FK CONSTRAINT     y   ALTER TABLE ONLY public.item_issued
    ADD CONSTRAINT item_id_fk FOREIGN KEY (item_id) REFERENCES public.inventory(id);
 @   ALTER TABLE ONLY public.item_issued DROP CONSTRAINT item_id_fk;
       public          postgres    false    2944    211    209            ?           2606    66335    maintenance_log item_id_fk    FK CONSTRAINT     }   ALTER TABLE ONLY public.maintenance_log
    ADD CONSTRAINT item_id_fk FOREIGN KEY (item_id) REFERENCES public.inventory(id);
 D   ALTER TABLE ONLY public.maintenance_log DROP CONSTRAINT item_id_fk;
       public          postgres    false    209    2944    215            ?           2606    66288    order ordered_by_fk    FK CONSTRAINT     w   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT ordered_by_fk FOREIGN KEY (ordered_by) REFERENCES public.users(id);
 ?   ALTER TABLE ONLY public."order" DROP CONSTRAINT ordered_by_fk;
       public          postgres    false    2934    213    201            ?           2606    57951    product posted_by_pk    FK CONSTRAINT        ALTER TABLE ONLY public.product
    ADD CONSTRAINT posted_by_pk FOREIGN KEY (posted_by) REFERENCES public.users(id) NOT VALID;
 >   ALTER TABLE ONLY public.product DROP CONSTRAINT posted_by_pk;
       public          postgres    false    2934    205    201            ?           2606    58025    inventory product_id_fk    FK CONSTRAINT     {   ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT product_id_fk FOREIGN KEY (product_id) REFERENCES public.product(id);
 A   ALTER TABLE ONLY public.inventory DROP CONSTRAINT product_id_fk;
       public          postgres    false    209    205    2940            ?           2606    58077    product_images product_id_fk    FK CONSTRAINT     ?   ALTER TABLE ONLY public.product_images
    ADD CONSTRAINT product_id_fk FOREIGN KEY (product_id) REFERENCES public.product(id) NOT VALID;
 F   ALTER TABLE ONLY public.product_images DROP CONSTRAINT product_id_fk;
       public          postgres    false    2940    207    205            ?           2606    58058    item_issued received_by_fk    FK CONSTRAINT     }   ALTER TABLE ONLY public.item_issued
    ADD CONSTRAINT received_by_fk FOREIGN KEY (received_by) REFERENCES public.users(id);
 D   ALTER TABLE ONLY public.item_issued DROP CONSTRAINT received_by_fk;
       public          postgres    false    201    2934    211            ?           2606    66340 $   maintenance_log status_updated_by_fk    FK CONSTRAINT     ?   ALTER TABLE ONLY public.maintenance_log
    ADD CONSTRAINT status_updated_by_fk FOREIGN KEY (status_updated_by) REFERENCES public.users(id);
 N   ALTER TABLE ONLY public.maintenance_log DROP CONSTRAINT status_updated_by_fk;
       public          postgres    false    215    201    2934            *   s   x?m̱? ????b)?ݘ???db??@?PS???8??-
r?\Q=??k?󉎗+?m?L~C{?O?u??UᐡrA???`?p:<?Hn????G?eG???Y??0-?q'o???@?(W      "   ?   x????? Dϸ?4????Z~?u|r?@??<yc??p??7??? l?)W-?&?%????E???"???;???:|?J??V??c^?0	???h?$=5??࣏???v?'??C}x???ت???H?>? ZJh?!?????zz???Y?l#02iمa>????U"?WD?;      $   ?  x??VMo?@=?_???X?????MnmӨQ{??S?@?I??Y??e)?,!??{3???*?P!L??	?bU4?5Gw?6??????_?vֈ??W??]??d?1T??m??Q??U??N?,&0??#?D??h?v??)??o?7Ղ???ߺ_?j Hw'H?bH\D+?jo?2?C7UY!w?v??~???mW???c?5????^6?s"p??HAT^*?h??I]V9????uTN?7ΰ?C<?xݬ???Ţ?ű??JB??ջ?F?X??ĲQ[??2A???#E3?R:4?U$?hj{ƣ7???IeJP?ɟq??Y???~?wO]+n???^??X?5??6e`?ܱ?	???@?*??T???d?$???g#U????k_0x???l!)h?~?#?GP?e?????'./z@)}޲+?)Xx?Oq?X??????U!hP?qg?"v?;0&5?+*ǩ???	t>d?G)4???5F@	??n?!'ʏ?V???G"??Ӳ???J<?0v?F?]?Чr??Nϭ???Kp?b ???e?l?j3??v??眪??|3?wu?S??<??kn;??#?=C$V(d??^ݯ"HOF@?L:^Z??4E?h?r?x?S#?<o?ԑ3oGm_?Q??&???~M?G???:??E?of-?????e)e??	?ስ???)]???#t??INӈ???c?ܮ?????+?<lW??͸<???W?!~???IJ??Ͱ/E?? ?Ć4??ǀ??\4??Ƞ?????d2??$?_      (   d  x??RKo?@>/?bn=???"!???4mbLz??? ??,]M?}??Pc6<?c??L????????????I?'???AG??j%Z?[?4ڂ?\k+??˶??cga?H+???^'?Ut??.?t??C??_EA???????Z*?B7e_?? ?{zBh䡶P??͒??h?\??3%?K8ײ??Gq??o??6???VH31?H/	=??ފ<X:?D?f?D?/<d???&in?t?f?VY?d?;k?jQ?jqBȍ~??M?T?/$>W?+@`04??S*??"?????7'V?~??z0??]?GR'??<??	?]???2???5?qn?7?0???o&?~o???̏?	??w??Hx?b      &      x?????? ? ?         D  x?}S?o?0~v??SHk~4II?`?Qi?c? x؋????cG???????u??Nv|????w??̿,`n???J?1??9X?????~?hʭ??E???܄}`G???7???<Z????????Tl?V:?FR4w????"{(l?X???ð?R???|;?&g??;??U?????"?????!?{E??OG?^?%??<*?Q???A?]

k?a????߹C?jW??s?U?+?sB+?#+%?J2k1??:*?????1????? ??????????=ܬ?i????/???σHlEMk_?>?*????n??/?K???Gd
?????`?N???D}??Aǧ??Pg?8??4v?????ʈ????)?=?s????Y:??q???$??l??kl?ض??z?̡?{??[???JT?P?`d??G?diB?ǫ@?W??	T?%$I???????? ???,7d'?l2?? ??i???`L.V?Vp?+΢???)Y?t?׺a?j ή.?????qD'xZ??8gڰ??p??H?q	"?Lq^???^????[??k?$??`0?X?Dl         F   x?3?t)??K?2?tJ,)I-??2??I,(?/?2??,RHN?M-J????,J?I-.V(J??/I?????? J??          ?   x???K?0?u??!???.?*?IP*AQI?_`U?x5??<Y?&VZh{/???:? ??Q?<?9U??;}?=?LSކ?:??H%]?=???3HVQe?ƕ????????'ɩ??Hc?ba伟ъL<?8ꞣ???L? ??O?":ْՁ?,ΜΣ???<kc?         ?  x???Mk1Eך??m???wV65tQ??@J?<==?S??C<.??ո??B?]ý ?
??i?ն??Q???8?Y?[???Ú?'5?c?x9:N?ou?}?~???*C??,A?? f????aD	B?,??KFL%j???TJ??^:?vt?/????O???w?n>?g?A ~~\1@??0;??!QB!m(J?)$,h? ??#Zo?$?%q%?˂??|mB?h?A]?????Ь?%:?R????#xm Z?:??4??Cs5??W?ӭ[O???2??&??s>??u???}?+ ?r??K?5??m??G?,??S4i??;?]? ??Ƥ?X?h???Y?2i?}?۠wץ??C~?}x?w?F?H@0ɚ??|d,͞3:???딓???V????6?i??u?u?w?Fݏ     