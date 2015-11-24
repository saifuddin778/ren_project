wget http://www.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.8.16.tar.gz
tar xvzf hdf5-1.8.16.tar.gz
rm hdf5-1.8.16.tar.gz

cd hdf5-1.8.16
./configure --prefix=/usr/local --enable-shared --enable-hl
make
make install

wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.1.3.tar.gz
tar xvzf netcdf-4.1.3.tar.gz
rm netcdf-4.1.3.tar.gz

wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4/zlib-1.2.8.tar.gz
tar xvzf zlib-1.2.8.tar.gz
rm zlib-1.2.8.tar.gz
cd zlib-1.2.8
./configure
make
make install

cd ..

cd netcdf-4.1.3
LDFLAGS=-L/usr/local/lib CPPFLAGS=-I/usr/local/include ./configure --enable-netcdf-4 --enable-dap --enable-shared --prefix=/usr/local
make
make install

pip install numpy

ldconfig

pip install netCDF4

echo "EVERYTHING DONE!!! NETCDF4 INSTALLED"

