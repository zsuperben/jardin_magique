/* Try to put your onfig management in there.   
|  /!\  Because arduino, advanced functions returning 
        custom types needs to be put in a header file.
                                                       */


// TODO Add a function to reconfigure this on the fly.
struct config {
    long unsigned int date ;
    long unsigned int ip; 
    short unsigned int num_plant;
    short unsigned int version;
    char* name;
    char* streamId;
    char* master;
    char* login;
    char* passwd;
    unsigned int plantids[];
}

config get_config(){
    config temp_config;
    return temp_config;
}

null* build_default_config(){
    config default_config =
        {
        get_unix_timestamp(),
                
        // finish intial config please !! 
        
        }
}

unsigned int get_unix_timestamp(){
    return random();
}
